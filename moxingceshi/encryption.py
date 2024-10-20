import numpy as np
from PIL import Image
import ctypes

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

def getk1_k2(x, y, dot, left, right, H, W, mark):
    Max_1 = max(H, W)
    k1 = np.zeros(dot + Max_1 + 1, dtype=np.int32)
    k2 = np.zeros(dot + Max_1 + 1, dtype=np.int32)
    licm_lib.getk1_k2(x, y, dot, left, right, 0, H, mark, k1, k2)
    return k1, k2

def encryption(image, key):
    H, W = image.shape[:2]  # 获取图片的高度和宽度
    key = key.replace(" ", "").split(",")
    x_value = float(key[0])
    y_value = float(key[1])
    dot = max(H, W) + 10
    Max = H * W

    x, y = getx_y(dot, Max, x_value, y_value)

    mark = True if H < W else False
    k1, k2 = getk1_k2(x, y, dot, 0, W, H, W, mark)
    image = np.array(image)

    # 行加密
    for n in range(H):
        for i in range(3):
            image[n, 0:W, i] = np.bitwise_xor(image[n, 0:W, i], k1[n])
        for i in range(3):
            buffer = image[n, 1:k2[n], i].copy()
            image[n, 1:W - k2[n], i] = image[n, k2[n] + 1:W, i].copy()
            image[n, W - k2[n] + 1:W, i] = buffer.copy()

    k1, k2 = getk1_k2(x, y, dot, 0, W, H, W, not mark)

    # 列加密
    for n in range(W):
        for i in range(3):
            image[0:H, n, i] = np.bitwise_xor(image[0:H, n, i], k1[n])
        for i in range(3):
            buffer = image[0:k2[n], n, i].copy()
            image[0:H - k2[n], n, i] = image[k2[n]:H, n, i]
            image[H - k2[n]:H, n, i] = buffer

    image = Image.fromarray(np.uint8(image))
    return image

# 读取图像并加密保存
image = Image.open("input/pt.jpg").convert("RGB")
image_array = np.array(image)
key = "0.1, 0.2"
encrypted_image = encryption(image_array,key)
encrypted_image.save("output/jiami.jpg")
