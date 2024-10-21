import math
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import re
import os
import ctypes
import time
# # 引入2D-licm映射

licm_lib = ctypes.CDLL("lib/2D_LICM.dll", winmode=0)

licm_lib.getx_y.restype = None
licm_lib.getx_y.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double,
                            np.ctypeslib.ndpointer(dtype=np.double, ndim=1, flags='C_CONTIGUOUS'),
                            np.ctypeslib.ndpointer(dtype=np.double, ndim=1, flags='C_CONTIGUOUS')]

licm_lib.getk1_k2.restype = None
licm_lib.getk1_k2.argtypes = [
    np.ctypeslib.ndpointer(dtype=np.double, ndim=1, flags='C_CONTIGUOUS'),
    np.ctypeslib.ndpointer(dtype=np.double, ndim=1, flags='C_CONTIGUOUS'),
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    np.ctypeslib.ndpointer(dtype=np.int32, ndim=1, flags='C_CONTIGUOUS'),
    np.ctypeslib.ndpointer(dtype=np.int32, ndim=1, flags='C_CONTIGUOUS')
]

def getx_y(dot, Max, x1, y1):
    x = np.zeros(dot + Max * 3 + 5)
    y = np.zeros(dot + Max * 3 + 5)
    licm_lib.getx_y(dot, Max, x1, y1, x, y)

    return x, y
def getk1_k2(x, y, dot, left, right, top, bottom, mark):
    Max_1 = max(max(left, right), max(top, bottom))
    k1 = np.zeros(dot + Max_1 + 1, dtype=np.int32)
    k2 = np.zeros(dot + Max_1 + 1, dtype=np.int32)
    licm_lib.getk1_k2(x, y, dot, left, right, top, bottom, mark, k1, k2)

    return k1, k2


def encryption(image, key):
    image = np.array(image.convert("RGB"))
    H, W = image.shape[:2]  # 获取图片的高度和宽度


    top = 0
    bottom = H
    left = 0
    right = W


    key = key.replace(" ", "")
    key = key.split(",")
    x_value = float(key[0])
    y_value = float(key[1])
    Max_1 = max(max(left, right), max(top, bottom))
    dot = Max_1 + 10
    Max = H * W

    x, y = getx_y(dot, Max, x_value, y_value)

    mark = True if H < W else False
    k1, k2 = getk1_k2(x, y, dot, left, right, top, bottom, mark)

    # 行加密
    for n in range(top, bottom):
        # 行混乱
        for i in range(3):
            image[n, left:right, i] = np.bitwise_xor(image[n, left:right, i], k1[n])

        # 行移位
        for i in range(3):
            buffer = image[n, left + 1:left + k2[n], i].copy()
            image[n, left + 1:right - k2[n], i] = image[n, left + k2[n] + 1:right, i].copy()
            image[n, right - k2[n] + 1:right, i] = buffer.copy()

    k1, k2 = getk1_k2(x, y, dot, left, right, top, bottom, not mark)

    # 列加密
    for n in range(left, right):
        # 列混乱
        for i in range(3):
            image[top:bottom, n, i] = np.bitwise_xor(image[top:bottom, n, i], k1[n])
        # 列移位
        for i in range(3):
            buffer = image[top:top + k2[n], n, i].copy()
            image[top:bottom - k2[n], n, i] = image[top + k2[n]:bottom, n, i]
            image[bottom - k2[n]:bottom, n, i] = buffer

    # 扩散
    en_image = np.zeros((H * W * 3), dtype=np.uint8)
    s1 = np.zeros((H * W * 3), dtype=np.uint8)
    s2 = np.zeros((H * W * 3), dtype=np.uint8)

    for n in range(H * W * 3):
        s1_value = x[dot - (H - n)] * 1000
        s2_value = y[dot - (W - n)] * 1000
        s1[n] = np.floor(s1_value) % H
        s2[n] = np.floor(s2_value) % W

    image_tmp = image[top:bottom, left:right, :].copy()

    # Check if image_tmp is empty
    if image_tmp.size == 0:
        raise ValueError("The sliced image_tmp is empty. Please check the bounds.")

    # 转为一维数组
    image_tmp = image_tmp.reshape((1, -1))

    en_image[0] = image_tmp[0, 0]

    for i in range(1, H * W * 3):
        en_image[i] = en_image[i - 1] ^ image_tmp[0, i] ^ s2[i]

    en_image = en_image.reshape((bottom - top, right - left, 3))
    image[top:bottom, left:right, :] = en_image[:, :].copy()

    image = Image.fromarray(np.uint8(image))
    return image


# 读取图像并加密保存
image = Image.open("input/pt2.bmp")
key = "0.11, 0.12"
encrypted_image = encryption(image, key)
encrypted_image.save("output/jiami.bmp")
