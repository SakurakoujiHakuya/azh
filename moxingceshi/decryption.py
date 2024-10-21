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
def getk1_k2(x, y, dot, left, right, top, bottom, mark):
    Max_1 = max(max(left, right), max(top, bottom))
    k1 = np.zeros(dot + Max_1 + 1, dtype=np.int32)
    k2 = np.zeros(dot + Max_1 + 1, dtype=np.int32)
    licm_lib.getk1_k2(x, y, dot, left, right, top, bottom, mark, k1, k2)

    return k1, k2


def decryption(image, key):
    # 加密范围的大小
    image = np.array(image.convert("RGB"))
    H, W = image.shape[:2]
    # Define encryption bounds
    top = 0
    bottom = H
    left = 0
    right = W

    key = key.replace(" ", "").split(",")
    x_value = float(key[0])
    y_value = float(key[1])
    Max_1 = max(max(left, right), max(top, bottom))

    dot = Max_1 + 10
    Max = H * W
    mark = True if H < W else False
    x, y = getx_y(dot, Max, x_value, y_value)

    k1, k2 = getk1_k2(x, y, dot, left, right, top, bottom, not mark)

    # Ensure k1 and k2 are converted to the appropriate type
    k1 = np.array(k1, dtype=np.int32)
    k2 = np.array(k2, dtype=np.int32)
    image = np.array(image)

    # 逆扩散
    image_tmp = np.zeros((H * W * 3), dtype=np.uint8)
    s1 = np.zeros((H * W * 3), dtype=np.uint8)
    s2 = np.zeros((H * W * 3), dtype=np.uint8)

    for n in range(H * W * 3):
        s1_value = x[dot - (H - n)] * 1000
        s2_value = y[dot - (W - n)] * 1000
        s1[n] = np.floor(s1_value) % H
        s2[n] = np.floor(s2_value) % W

    en_image = image[top:bottom, left:right, :].copy()
    en_image = en_image.reshape((1, -1))
    image_tmp[0] = en_image[0, 0]

    for i in range(1, H * W * 3):
        image_tmp[i] = en_image[0, i - 1] ^ en_image[0, i] ^ s2[i]

    image_tmp = image_tmp.reshape((bottom - top, right - left, 3))
    image[top:bottom, left:right, :] = image_tmp[:, :, :].copy()

    # 列解密
    for n in range(left, right):
        # 列反移位
        for i in range(3):
            buffer = image[bottom - k2[n]:bottom, n, i].copy()
            image[top + k2[n]:bottom, n, i] = image[top:bottom - k2[n], n, i]
            image[top:top + k2[n], n, i] = buffer
        # 列反混乱
        for i in range(3):
            image[top:bottom, n, i] = np.bitwise_xor(image[top:bottom, n, i], k1[n])

    k1, k2 = getk1_k2(x, y, dot, left, right, top, bottom, mark)

    # 行解密
    for n in range(top, bottom):
        # 行反移位
        for i in range(3):
            buffer = image[n, left + 1:right - k2[n], i].copy()
            image[n, left + 1:left + k2[n], i] = image[n, right - k2[n] + 1:right, i]
            image[n, left + k2[n] + 1:right, i] = buffer

        # 行反混乱
        for i in range(3):
            image[n, left:right, i] = np.bitwise_xor(image[n, left:right, i], k1[n])

    image = Image.fromarray(np.uint8(image))
    return image


# 读取图像并解密保存
image = Image.open("input/pt3.bmp")
key = "0.11, 0.12"
decrypted_image = decryption(image, key)
decrypted_image.save("output/jiemi.bmp")