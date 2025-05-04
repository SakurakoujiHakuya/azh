import cv2
import numpy as np
import json
import os

def run_NPCR_UACI_BACI():
    # 读取图像（灰度模式）
    P1 = cv2.imread('input/pt2.bmp', cv2.IMREAD_GRAYSCALE)
    P2 = cv2.imread('output/jiami.bmp', cv2.IMREAD_GRAYSCALE)

    if P1 is None or P2 is None:
        raise FileNotFoundError("图像文件未找到，请检查路径")

    # 检查尺寸是否一致
    if P1.shape != P2.shape:
        raise ValueError("图像尺寸不一致，请检查输入")

    # 调用指标计算函数
    npcr, uaci, baci = NPCR_UACI_BACI(P1, P2)

    # # 打印结果
    # print(f"🔐 NPCR: {npcr:.4f}%")
    # print(f"🎨 UACI: {uaci:.4f}%")
    # print(f"📊 BACI: {baci:.4f}%")

    # 保存结果为 JSON 文件
    save_results_as_json(npcr, uaci, baci)

def NPCR_UACI_BACI(P1, P2):
    P1 = P1.astype(np.float64)
    P2 = P2.astype(np.float64)
    M, N = P1.shape

    # NPCR
    D = (P1 != P2)
    NPCR = np.sum(D) / (M * N) * 100

    # UACI
    UACI = np.sum(np.abs(P1 - P2)) / (255 * M * N) * 100

    # BACI
    diff = np.abs(P1 - P2)
    m = 0.0
    for i in range(M - 1):
        for j in range(N - 1):
            d = diff[i:i+2, j:j+2]
            baci_sum = (
                abs(d[0, 0] - d[0, 1]) +
                abs(d[0, 0] - d[1, 0]) +
                abs(d[0, 0] - d[1, 1]) +
                abs(d[0, 1] - d[1, 0]) +
                abs(d[0, 1] - d[1, 1]) +
                abs(d[1, 0] - d[1, 1])
            )
            m += baci_sum / 6.0 / 255.0
    BACI = m / ((M - 1) * (N - 1)) * 100

    return NPCR, UACI, BACI

def save_results_as_json(npcr, uaci, baci):
    # 创建结果字典
    results = {
        "NPCR": round(npcr, 4),
        "UACI": round(uaci, 4),
        "BACI": round(baci, 4)
    }

    # 确保输出目录存在
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # 保存为 JSON 文件
    output_file = os.path.join(output_dir, "npcr_uaci_baci_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"结果已保存到 {output_file}")

# 运行示例
if __name__ == "__main__":
    try:
        run_NPCR_UACI_BACI()
    except Exception as e:
        print(f"脚本运行时出错: {e}")