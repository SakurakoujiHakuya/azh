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

def decryption(image, key):
    H, W = image.shape[:2]  # 获取图片的高度和宽度
    key = key.replace(" ", "").split(",")
    x_value = float(key[0])
    y_value = float(key[1])
    dot = max(H, W) + 10
    Max = H * W

    x, y = getx_y(dot, Max, x_value, y_value)

    mark = True if H < W else False
    k1, k2 = getk1_k2(x, y, dot, 0, W, H, W, not mark)
    image = np.array(image)

    # 逆扩散
    image_tmp = np.zeros((H * W * 3), dtype=np.uint8)
    s1 = np.zeros((H * W * 3), dtype=np.uint8)
    s2 = np.zeros((H * W * 3), dtype=np.uint8)

    en_image = image[0:H, 0:W, :].copy()
    en_image = en_image.reshape((1, -1))
    image_tmp[0] = en_image[0, 0]
    for i in range(1, H * W * 3):
        image_tmp[i] = en_image[0, i - 1] ^ en_image[0, i] ^ s2[i]

    image_tmp = image_tmp.reshape((H, W, 3))
    image[0:H, 0:W, :] = image_tmp[:, :, :].copy()

    # 列解密
    for n in range(W):
        for i in range(3):
            buffer = image[H - k2[n]:H, n, i].copy()
            image[k2[n]:H, n, i] = image[0:H - k2[n], n, i]
            image[0:k2[n], n, i] = buffer
        for i in range(3):
            image[0:H, n, i] = np.bitwise_xor(image[0:H, n, i], k1[n])

    k1, k2 = getk1_k2(x, y, dot, 0, W, H, W, mark)

    # 行解密
    for n in range(H):
        for i in range(3):
            buffer = image[n, 1:W - k2[n], i].copy()
            image[n, 1:1 + k2[n], i] = image[n, W - k2[n] + 1:W, i]
            image[n, 1 + k2[n]:W, i] = buffer

            # 行反混乱
        for i in range(3):
            image[n, 0:W, i] = np.bitwise_xor(image[n, 0:W, i], k1[n])

        image = Image.fromarray(np.uint8(image))
        return image

    # 读取图像并解密保存
    image = Image.open("input/pt.jpg")
    key = "0.1, 0.2"
    decrypted_image = decryption(image, key)
    decrypted_image.save("output/jiemi.jpg")

