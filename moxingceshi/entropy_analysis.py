import cv2
import numpy as np
import math
import json
import os

def run_entropy_analysis():
    # 固定图片路径为 output/jiami.bmp
    file_path = 'output/jiami.bmp'

    # 1. 检查文件是否存在并读取图像（保持为彩色）
    img = cv2.imread(file_path)
    if img is None or len(img.shape) != 3 or img.shape[2] != 3:
        raise ValueError(f"图像 {file_path} 不是 RGB 彩色图，请检查路径或文件内容")

    # OpenCV 读入是 BGR 顺序，需转换为 RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 2. 计算信息熵
    entropy_rgb = compute_entropy_rgb(img)

    # 检查熵值是否有效
    if not entropy_rgb or len(entropy_rgb) != 3:
        raise ValueError("计算的信息熵结果无效，请检查图像数据或计算逻辑")

    # 3. 输出结果保存为 JSON 文件
    save_entropy_as_json(entropy_rgb)

def compute_entropy_rgb(image):
    entropy = []
    for i in range(3):  # R, G, B 通道
        channel = image[:, :, i]
        hist = cv2.calcHist([channel], [0], None, [256], [0, 256]).flatten()
        hist_sum = np.sum(hist)
        if hist_sum == 0:  # 防止除以零
            print(f"警告：通道 {i} 的直方图总和为 0，信息熵设为 0")
            entropy.append(0)
            continue
        probs = hist / hist_sum

        # 计算信息熵，忽略概率为 0 的值
        channel_entropy = -np.sum([p * math.log2(p) for p in probs if p > 0])
        entropy.append(channel_entropy)
    print(f"调试：计算得到的熵值为 {entropy}")
    return entropy

def save_entropy_as_json(entropy_rgb):
    # 创建结果字典
    results = {
        "Entropy_R": round(float(entropy_rgb[0]), 4),  # 转换为 Python float
        "Entropy_G": round(float(entropy_rgb[1]), 4),  # 转换为 Python float
        "Entropy_B": round(float(entropy_rgb[2]), 4)   # 转换为 Python float
    }

    # 确保输出目录存在
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # 保存为 JSON 文件
    output_file = os.path.join(output_dir, "entropy_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"信息熵结果已保存到 {output_file}")

# 执行主程序
if __name__ == "__main__":
    run_entropy_analysis()