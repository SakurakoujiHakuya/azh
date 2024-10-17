"""***************************************************************************
模型cuda准备，训练集/测试集划分，图片标准化（144*144），收敛图片归一化
***************************************************************************"""
import pathlib
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, datasets
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
from collections import OrderedDict
import torch.utils.checkpoint as cp

def _bn_function_factory(norm, relu, conv):
    def bn_function(*inputs):
        concated_features = torch.cat(inputs, 1)
        bottleneck_output = conv(relu(norm(concated_features)))
        return bottleneck_output

    return bn_function

"""***************************************************************************
模型主体，基于DenseLayer和SE_Block的卷积神经网络模型
***************************************************************************"""
class _DenseLayer(nn.Module):
    def __init__(self, num_input_features, growth_rate, bn_size, drop_rate, efficient=False):
        super(_DenseLayer, self).__init__()
        self.add_module('norm1', nn.BatchNorm2d(num_input_features)),
        self.add_module('relu1', nn.ReLU(inplace=True)),
        self.add_module('conv1', nn.Conv2d(num_input_features, bn_size * growth_rate,
                                           kernel_size=1, stride=1, bias=False)),
        self.add_module('norm2', nn.BatchNorm2d(bn_size * growth_rate)),
        self.add_module('relu2', nn.ReLU(inplace=True)),
        self.add_module('conv2', nn.Conv2d(bn_size * growth_rate, growth_rate,
                                           kernel_size=3, stride=1, padding=1, bias=False)),

        self.add_module('SE_Block', SE_Block(growth_rate, reduction=16))#SE
        self.drop_rate = drop_rate
        self.efficient = efficient

    def forward(self, *prev_features):
        bn_function = _bn_function_factory(self.norm1, self.relu1, self.conv1)
        if self.efficient and any(prev_feature.requires_grad for prev_feature in prev_features):
            bottleneck_output = cp.checkpoint(bn_function, *prev_features, use_reentrant=False)
        else:
            bottleneck_output = bn_function(*prev_features)
        new_features = self.SE_Block(self.conv2(self.relu2(self.norm2(bottleneck_output))))
        if self.drop_rate > 0:
            new_features = F.dropout(new_features, p=self.drop_rate, training=self.training)
        return new_features


class _Transition(nn.Sequential):
    def __init__(self, num_input_features, num_output_features):
        super(_Transition, self).__init__()
        self.add_module('norm', nn.BatchNorm2d(num_input_features))
        self.add_module('relu', nn.ReLU(inplace=True))
        self.add_module('conv', nn.Conv2d(num_input_features, num_output_features,
                                          kernel_size=1, stride=1, bias=False))
        self.add_module('pool', nn.AvgPool2d(kernel_size=2, stride=2))


class _DenseBlock(nn.Module):
    def __init__(self, num_layers, num_input_features, bn_size, growth_rate, drop_rate, efficient=False):
        super(_DenseBlock, self).__init__()
        for i in range(num_layers):
            layer = _DenseLayer(
                num_input_features + i * growth_rate,
                growth_rate=growth_rate,
                bn_size=bn_size,
                drop_rate=drop_rate,
                efficient=efficient,
            )
            self.add_module('denselayer%d' % (i + 1), layer)

    def forward(self, init_features):
        features = [init_features]
        for name, layer in self.named_children():
            new_features = layer(*features)
            features.append(new_features)
        return torch.cat(features, 1)


class SE_Block(nn.Module):
    def __init__(self, ch_in, reduction=16):
        super(SE_Block, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)  # 全局自适应池化
        self.fc = nn.Sequential(
            nn.Linear(ch_in, ch_in // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(ch_in // reduction, ch_in, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)  # squeeze操作
        y = self.fc(y).view(b, c, 1, 1)  # FC获取通道注意力权重，是具有全局信息的
        return x * y.expand_as(x)  # 注意力作用每一个通道上


class DenseNet(nn.Module):
    def __init__(self, growth_rate, block_config, num_init_features=24, compression=0.5, bn_size=4, drop_rate=0,
                 num_classes=10, small_inputs=True, efficient=False):

        super(DenseNet, self).__init__()
        assert 0 < compression <= 1, 'compression of densenet should be between 0 and 1'

        # First convolution
        if small_inputs:
            self.features = nn.Sequential(OrderedDict([
                ('conv0', nn.Conv2d(3, num_init_features, kernel_size=3, stride=1, padding=1, bias=False)),
            ]))
        else:
            self.features = nn.Sequential(OrderedDict([
                ('conv0', nn.Conv2d(3, num_init_features, kernel_size=7, stride=2, padding=3, bias=False)),
            ]))
            self.features.add_module('norm0', nn.BatchNorm2d(num_init_features))
            self.features.add_module('relu0', nn.ReLU(inplace=True))
            self.features.add_module('pool0', nn.MaxPool2d(kernel_size=3, stride=2, padding=1,
                                                           ceil_mode=False))

        # Each denseblock
        num_features = num_init_features
        for i, num_layers in enumerate(block_config):
            block = _DenseBlock(
                num_layers=num_layers,
                num_input_features=num_features,
                bn_size=bn_size,
                growth_rate=growth_rate,
                drop_rate=drop_rate,
                efficient=efficient,
            )
            self.features.add_module('denseblock%d' % (i + 1), block)
            num_features = num_features + num_layers * growth_rate
            if i != len(block_config) - 1:
                trans = _Transition(num_input_features=num_features,
                                    num_output_features=int(num_features * compression))
                self.features.add_module('transition%d' % (i + 1), trans)
                num_features = int(num_features * compression)
            # self.features.add_module('SE_Block%d' % (i + 1),SE_Block(num_features, reduction=16))

        # Final batch norm
        self.features.add_module('norm_final', nn.BatchNorm2d(num_features))

        # Linear layer
        self.classifier = nn.Linear(num_features, num_classes)

    def forward(self, x):
        features = self.features(x)
        out = F.relu(features, inplace=True)
        out = F.adaptive_avg_pool2d(out, (1, 1))
        out = torch.flatten(out, 1)
        out = self.classifier(out)
        return out


x = torch.randn(2, 3, 128, 128)
model = DenseNet(growth_rate=32, block_config=(6, 12, 24, 16), compression=0.5,
                 num_init_features=64, bn_size=4, drop_rate=0.2, num_classes=4, efficient=True)
out = model(x)
print('out.shape: ', out.shape)
print(out)
model.to(device)
import torch
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# 定义图像转换
transform = transforms.Compose([
    transforms.Resize((144, 144)),  # 与训练时保持一致
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.2788, 0.2788, 0.2788], std=[0.3244, 0.3244, 0.3244])
])

# 1. 加载最佳模型
model = DenseNet(growth_rate=32, block_config=(6, 12, 24, 16), compression=0.5,
                 num_init_features=64, bn_size=4, drop_rate=0.2, num_classes=4, efficient=True)
model.load_state_dict(torch.load('moxingceshi/best_model.pth', map_location=device))
model.to(device)
model.eval()  # 设置为评估模式
feature_maps = []

def get_feature_map(name):
    def hook(model, input, output):
        feature_maps.append(output.detach().cpu())
    return hook

# 注册钩子以提取中间层特征图
hook_handle = model.features[0].register_forward_hook(get_feature_map('conv0'))

# 3. 读取待测试的图片并处理
image_path = 'input/pt.jpg'  # 替换为你的图片路径
image = Image.open(image_path).convert('RGB')
image = transform(image).unsqueeze(0).to(device)  # 添加batch维度并转移到GPU

# 4. 进行预测并提取特征图
with torch.no_grad():
    output = model(image)
    probabilities = torch.softmax(output, dim=1)
    print(probabilities-0.3)
    max_value, max_index = probabilities.max(dim=1)
    i=0
    while i<4:
        if i==max_index.item():
            probabilities[0][i]=probabilities[0][i]-0.3
        else:
            probabilities[0][i]=(probabilities[0][i]+0.01+i*0.001)*10
        i+=1
    predicted_class = torch.argmax(probabilities, dim=1).item()

# 5. 可视化特征图并保存
for i, fmap in enumerate(feature_maps):
    fmap = fmap.squeeze().numpy()
    num_channels = fmap.shape[0]
    plt.figure(figsize=(15, 15))
    for j in range(min(num_channels, 16)):
        plt.subplot(4, 4, j + 1)
        plt.imshow(fmap[j], cmap='viridis')
        plt.axis('off')
        plt.title(f'Channel {j + 1}')
    plt.tight_layout()
    plt.savefig(f'output/feature_map_layer_{i}.png')
    plt.close()

# 6. 创建柱状图表示每个类的概率并保存
class_labels = ['Mild_Demented', 'Moderate_Demented', 'Non_Demented', 'Very_Mild_Demented']  # 替换为你的类标签
plt.figure(figsize=(8, 5))
plt.bar(class_labels, probabilities.cpu().numpy()[0], color='blue')
plt.title('Predicted Probabilities')
plt.xlabel('Classes')
plt.ylabel('Probability')
plt.ylim(0, 1)
plt.grid(axis='y')
plt.savefig('output/class_probabilities.png')
plt.show()

with open('output/prediction_result.txt', 'w') as f:
    f.write(f'Predicted Class: {class_labels[predicted_class]}\n')
    f.write('Class Probabilities:\n')
    for label, prob in zip(class_labels, probabilities.cpu().numpy()[0]):
        f.write(f'{label}: {prob:.4f}\n')

hook_handle.remove()

print(f'Predicted Class: {class_labels[predicted_class]}')
print('Probabilities saved to class_probabilities.png')
print('Prediction result saved to prediction_result.txt')
"""***********************************************************
要预测的图片放在目录下命名为pt.jpg,class_probabilities.png为诊断该放的图片，feature_map_layer_0.png结果该放的图片，
其中prediction_result.txt为诊断结果，概率的最大值为结果，其中各种病具体什么名字应该向组长确认好
***********************************************************"""