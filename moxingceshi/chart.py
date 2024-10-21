import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def create_histogram(image):
    image = np.array(image.convert("RGB"))
    H, W = image.shape[:2]
    top = 0
    bottom = H
    left = 0
    right = W

    image_en = image[top:bottom, left:right, :]
    # 转换为RGB格式
    image_rgb = cv.cvtColor(image_en, cv.COLOR_RGB2BGR)
    fig, ax = plt.subplots()

    # 绘制RGB通道的直方图
    ax.hist(image_rgb[:, :, 0].ravel(), bins=60, color='r', alpha=0.7, label='Red', density=False)
    ax.hist(image_rgb[:, :, 1].ravel(), bins=60, color='g', alpha=0.7, label='Green', density=False)
    ax.hist(image_rgb[:, :, 2].ravel(), bins=60, color='b', alpha=0.7, label='Blue', density=False)

    # 设置x轴范围
    ax.set_xlim([0, 256])

    ax.legend()

    # 返回生成的图形对象
    return fig

# 读取图像并生成直方图
image = Image.open("output/jiami.bmp")
fig = create_histogram(image)
fig.savefig("output/histogram.jpg")
plt.close(fig)  # 关闭图形以释放内存

