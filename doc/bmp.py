from struct import unpack
from enum import Enum
import PIL.Image

class BfType(Enum):
    BM = b'BM'  # Windows 3.1x, 95, NT, ...
    BA = b'BA'  # OS/2 Bitmap Array
    CI = b'CI'  # OS/2 Color Icon
    CP = b'CP'  # OS/2 Color Pointer
    IC = b'IC'  # OS/2 Icon
    PT = b'PT'  # OS/2 Pointer

class BiCompression(Enum):
    BI_RGB = 0          # 不压缩（常用）
    BI_RLE8 = 1         # 8bit游程编码，只用于8位 位图
    BI_RLE4 = 2         # 4bit游程编码，只用于4位 位图
    BI_BITFIELDS = 3    # bit域，用于16位/32位 位图
    BI_JPEG = 4         # 位图含JPEG图像（仅用于打印机）
    BI_PNG = 5          # 位图含PNG图像（仅用于打印机）

def read_header(f):
    bfType = f.read(2)                      # 文件类型
    bfSize = unpack('<i', f.read(4))[0]     # 文件大小
    _bfReserverd1 = f.read(2)
    _bfReserverd2 = f.read(2)
    bfOffBits = unpack('<i', f.read(4))[0]  # 从文件头到位图数据部分的偏移量
    return (bfType, bfSize, bfOffBits)

def read_file(path: str):
    with open(path, 'rb') as f:
        # file header 14bytes
        (bfType, bfSize, bfOffBits) = read_header(f)
        print(BfType(bfType), f'File Size: {bfSize}', f'Data Offset: {bfOffBits}')
        # bitmap infomation 40bytes
        biSize = unpack('<i', f.read(4))[0]                         # infomation 部分的字节数
        biWidth = unpack('<i', f.read(4))[0]                        # 图像宽度（像素）
        biHeight = unpack('<i', f.read(4))[0]                       # 图像高度（像素）
        biPlanes = unpack('<h', f.read(2))[0]                       # 颜色平面数
        biBitCount = unpack('<h', f.read(2))[0]                     # 像素位宽
        biCompression = BiCompression(unpack('<i', f.read(4))[0])   # 压缩类型
        biSizeImage = unpack('<i', f.read(4))[0]                    # 图像大小（字节）
        biXPelsPerMeter = unpack('<i', f.read(4))[0]                # 水平分辨率（像素/米）
        biYPelsPerMeter = unpack('<i', f.read(4))[0]                # 垂直分辨率（像素/米）
        biClrUsed = unpack('<i', f.read(4))[0]                      # 颜色索引数
        biClrImportant = unpack('<i', f.read(4))[0]                 # 颜色索引数（重要）
        # print(biSize, biWidth, biHeight, biCompression, biBitCount, biSizeImage)
        if biSizeImage % 4 != 0:
            print(f'SizeImage Error: {biSizeImage} % 4 != 0')
        # bitmap data
        pixels = []
        for row in range(biHeight):
            for col in range(biWidth):
                b = unpack('<B', f.read(1))[0]
                g = unpack('<B', f.read(1))[0]
                r = unpack('<B', f.read(1))[0]
                pixels.append((r, g, b))
            # pixels.append(line)
            pad_count = biWidth % 4
            _ = f.read(pad_count)
        pixels.reverse()
        img = PIL.Image.new('RGB', (biWidth, biHeight))
        img.putdata(pixels)
        img.show()

if __name__ == '__main__':
    read_file(f'./img/suey.bmp')