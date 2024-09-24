# Jpeg Segments
# Abbr  Marker  Name                        Describe
# SOI   0xFFD8  Start of Image              文件开始
# SOF0  0xFFC0  Baseline DCT-based JPEG
# SOF2  0xFFC2  Progressive DCT-based JPEG
# DHT   0xFFC4  Define Huffman Tables
# DQT   0xFFDB  Define Quantization Table
# DRI   0xFFDD  Define Restart Interval     定义RSTn的MCU间隔数N
# SOS   0xFFDA  Start of Scan               图像数据开始
# RSTn  0xFFDn  Restart                     每间隔N个MCU就会有一个RST0～7循环
# APPn  0xFFEn  Application-specific        Exif JPEG使用APP1, JFIF JPEG使用APP0
# COM   0xFFFE  Comment                     注释内容
# EOI   0xFFD9  End of Image                文件结束

from enum import Enum
from struct import unpack

class SOI:
    'Start of image'
    def __init__(self, segment: bytes) -> None:
        if segment != [0xD8]:
            raise ValueError("SOI Read Error")

class EOI:
    'End of Image'
    def __init__(self, segment: bytes) -> None:
        if segment != [0xD9]:
            raise ValueError("EOI Read Error")

class DensityUnit(Enum):
    Unknown = 0
    Pixel_Inch = 1
    Pixel_Cm = 2

class APP0:
    'Application-specific 0'
    # 标记代码｜｜  2 bytes 固定值：0xFFE0
    # 数据长度｜｜  2 bytes 包含自身但不包含标记代码
    # 标识符｜｜｜  5 bytes Identifier 固定长度字符串："JFIF\0"
    # 版本号｜｜｜  2 bytes 一般为0x0101或0x0102，表示1.1或1.2
    # 像素单位｜｜  1 byte
    #       0 没有单位
    #       1 pixel/inch
    #       2 pixel/cm
    # 水平像素数目｜    2 bytes
    # 垂直像素数目｜    2 bytes
    # 缩略图像素数目    2 bytes
    #       1 byte 水平
    #       1 byte 垂直
    # 缩略图位图 3n bytes
    # n = 缩略图水平像素数目*缩略图垂直像素数目
    # 这是一个24bits/pixel的RGB位图
    def __init__(self, segment: bytes) -> None:
        _ = segment[0]  # marker
        length = unpack('>H', bytes(segment[1:3]))[0]
        self.identifier = unpack('5s', bytes(segment[3:8]))
        self.version = unpack('>H', bytes(segment[8:10]))[0]
        self.unit = DensityUnit(unpack('B', bytes(segment[10:11]))[0])
        self.density_row = unpack('>H', bytes(segment[11:13]))[0]
        self.density_col = unpack('>H', bytes(segment[13:15]))[0]
        self.thumbnail_row = unpack('B', bytes(segment[15:16]))[0]
        self.thumbnail_col = unpack('B', bytes(segment[16:17]))[0]
        self.thumbnail = segment[17:]
        if len(self.thumbnail) != self.thumbnail_row * self.thumbnail_col * 3:
            raise ValueError('thumbnail Length Error')
        if length != 16 + len(self.thumbnail):
            raise ValueError(f'SOF0 Length Error, Expect({length}), Read({16 + len(self.thumbnail)})')
        print(f'===== APP0 length: {length} =====')
        print('Identifier:', self.identifier)
        print('Version:', hex(self.version))
        print('Unit:', self.unit)
        print('Image Density Width x Heigth:', self.density_row, self.density_col)
        print('thumbnail Width x Heigth:', self.thumbnail_row, self.thumbnail_col)

class APPn:
    'Application-specific n'
    # 标记代码｜｜  2 bytes 固定值：0xFFEn(1~F)
    # 数据长度｜｜  2 bytes 包含自身但不包含标记代码
    # 详细信息｜｜  (length - 2) bytes
    #       Exif使用APP1来存放图片的metadata
    #       Adobe Photoshop用APP1和APP13两个标记段分别存储了一副图像的副本
    def __init__(self, segment: bytes) -> None:
        print('APPn Len:', len(segment))

class SOF0:
    'Start of Frame0 Baseline DCT-based JPEG'
    # 标记代码｜｜  2 bytes 固定值：0xFFC0
    # 数据长度｜｜  2 bytes 包含自身但不包含标记代码
    # 精度｜｜｜｜  1 byte  每个样本数据的位数，通常是8位
    # 图像高度｜｜  2 bytes 单位：像素
    # 图像宽度｜｜  2 bytes 单位：像素
    # 颜色分量数｜  1 bytes 灰度级1，YCbCr或YIQ是3，CMYK是4
    # 颜色分量信息  颜色分量数 * 3 bytes
    #       1 byte 分量ID
    #       1 byte 采样因子（前4位：水平采样，后4位：垂直采样）
    #       1 byte 当前分量使用的量化表ID
    def __init__(self, segment: bytes) -> None:
        _ = segment[0]  # marker
        length = unpack('>H', bytes(segment[1:3]))[0]
        self.degree = unpack('B', bytes(segment[3:4]))[0]
        self.height = unpack('>H', bytes(segment[4:6]))[0]
        self.width = unpack('>H', bytes(segment[6:8]))[0]
        self.vector_count = unpack('B', bytes(segment[8:9]))[0]
        self.vector_info = []
        for count in range(self.vector_count):
            vector_id = segment[9 + count * 3]
            sample_factor = segment[10 + count * 3]
            vertical_factor = sample_factor & 0x0F
            horizontal_factor = sample_factor >> 4
            dqt_id = segment[11 + count * 3]
            self.vector_info.append((vector_id, horizontal_factor, vertical_factor, dqt_id))
        if length != 11 + (self.vector_count - 1) * 3:
            raise ValueError(f'SOF0 Length Error, Expect({length}), Read({(self.vector_count - 1) * 3})')
        print(f'===== SOF0 length: {length} =====')
        print('Sample Degree:', self.degree)
        print('Image Width x Heigth:', self.height, self.width)
        print('Vector Info:', self.vector_info)

class SOF2:
    'Start of Frame2 Progressive DCT-based JPEG'
    def __init__(self, segment: bytes) -> None:
        print('SOF2 Len:', len(segment))

class HuffmanTableType(Enum):
    DC = 0
    AC = 1

class DHT:
    'Define Huffman Tables'
    # 标记代码｜｜  2 bytes 固定值：0xFFC4
    # 数据长度｜｜  2 bytes 包含自身但不包含标记代码
    # 哈夫曼表｜｜  (length - 2) bytes
    #       表ID和表类型  1 byte
    #       	高4位：类型，只有两个值可选，0为DC直流，1为AC交流
    #           低4位：哈夫曼表ID，注意DC表和AC表是分开编码的
    #       不同位数的码字数量 16 bytes
    #       编码内容  上述16个不同位数的码字的数量和 bytes
    def __init__(self, segment: bytes) -> None:
        _ = segment[0]  # marker
        length = unpack('>H', bytes(segment[1:3]))[0]
        value = unpack('B', bytes(segment[3:4]))[0]
        self.id = value & 0x0F
        self.table_type = HuffmanTableType(value >> 4)
        self.counts = segment[4:20]
        self.tables = []
        all_counts = 0
        for count in self.counts:
            self.tables.append(segment[20 + all_counts: 20 + all_counts + count])
            all_counts += count
        if length != 19 + all_counts:
            raise ValueError(f'SOF0 Length Error, Expect({length}), Read({19 + all_counts})')

        print(f'===== DHT length: {length} =====')
        print(f'DHT ID: {self.id}, Type: {self.table_type}, Counts: {all_counts}')

class QuantizationDegree(Enum):
    Bits8 = 0
    Bits16 = 1

class DQT:
    'Define Quantization Table'
    # 标记代码｜｜  2 bytes 固定值：0xFFDB
    # 数据长度｜｜  2 bytes 包含自身但不包含标记代码
    # 量化表｜｜｜  （length - 2） bytes
    #       精度和ID  1 byte
    #               高4位为精度，只有两个可选值：0表示8bits，1表示16bits
    #               低4位为量化表ID，取值范围为0~3
    #       表项  64 * (精度 + 1)bytes
    #           8bits  64 * (0 + 1)bytes = 64 bytes
    #           16bits  64 * (1 + 1)bytes 128 bytes
    def __init__(self, segment: bytes) -> None:
        _ = segment[0]  # marker
        length = unpack('>H', bytes(segment[1:3]))[0]
        value = unpack('B', bytes(segment[3:4]))[0]
        self.id = value & 0x0F
        self.degree = QuantizationDegree(value >> 4)
        self.table = segment[4:4 + 64 * (self.degree.value + 1)]
        if length != 3 + len(self.table):
            raise ValueError(f'SOF0 Length Error, Expect({length}), Read({3 + len(self.table)})')

        print(f'===== DQT length: {length} =====')
        print(f'DQT ID: {self.id}, Degree: {self.degree}')

class DRI:
    'Define Restart Interval ST中的marker'
    # 标记代码｜｜  2 bytes 固定值：0xFFDD
    # 数据长度｜｜  2 bytes 固定值0x0004
    # MCU块的单元中的重新开始间隔
    #   设其值为n，则表示每n个MCU块就有一个RSTn标记
    #   第一个标记是RST0，第二个是RST1等，RST7后再从RST0重复。
    def __init__(self, segment: bytes) -> None:
        _ = segment[0]  # marker
        length = unpack('>H', bytes(segment[1:3]))[0]
        self.interval = unpack('>H', bytes(segment[3:5]))[0]
        if length != 4:
            raise ValueError(f'SOF0 Length Error, Expect({length}), Read(4)')

        print(f'===== DRI length: {length} =====')
        print('MCU Interval:', self.interval)

class SOS:
    'Start of Scan'
    # 标记代码｜｜  2 bytes 固定值：0xFFDA
    # 数据长度｜｜  2 bytes 包含自身但不包含标记代码
    # 颜色分量数｜  1 bytes 灰度级1，YCbCr或YIQ是3，CMYK是4
    # 颜色分量信息  颜色分量数 * 3 bytes
    #       1 byte 分量ID
    #       1 byte 直流/交流系数表号
    #           高4位：直流分量使用的哈夫曼树编号（direct-current）
    #           低4位：交流分量使用的哈夫曼树编号(alternating-current)
    # 压缩图像信息  3bytes
    #       1 byte 谱选择开始 固定为0x00
    #       1 byte 谱选择结束 固定为0x3f
    #       1 byte 谱选择 在basic JPEG中固定为00
    def __init__(self, segment: bytes) -> None:
        _ = segment[0]  # marker
        length = unpack('>H', bytes(segment[1:3]))[0]
        self.vector_count = unpack('B', bytes(segment[3:4]))[0]
        self.vector_info = []
        for count in range(self.vector_count):
            vector_id = segment[4 + count * 2]
            dht_id = segment[5 + count * 2]
            ac = dht_id & 0x0F
            dc = dht_id >> 4
            self.vector_info.append((vector_id, dc, ac))
        self.thumbnail_spectrum_start = segment[4 + self.vector_count * 2]
        self.thumbnail_spectrum_end = segment[5 + self.vector_count * 2]
        self.thumbnail_spectrum_select = segment[6 + self.vector_count * 2]
        if self.thumbnail_spectrum_start != 0x00 \
            or self.thumbnail_spectrum_end != 0x3F:
                raise ValueError('Thumbnail Spectrum Error')
        if length != 6 + self.vector_count * 2:
            raise ValueError(f'SOF0 Length Error, Expect({length}), Read({6 + self.vector_count * 2})')
        print(f'===== SOF0 length: {length} =====')
        print('Vector Info:', self.vector_info)
        print('Thumbnail Spectrum Select:', self.thumbnail_spectrum_select)

class COM:
    'Comment'
    def __init__(self, segment: bytes) -> None:
        print('COM Len:', len(segment))

class Frame:
    pass

class Jpeg:
    def _read_segments(content: bytes):
        segments = []
        segment = []
        flag = False
        for byte in content:
            if byte == 0xFF:
                flag = True
            else:
                if flag is False:
                    segment.append(byte)
                else:
                    flag = False
                    if byte == 0x00:
                        segment.append(0xFF)
                    elif byte == 0xFF:
                        continue
                    elif byte == 0xD8:
                        segment = [0xD8]
                    elif byte == 0xD9:
                        segments.append([0xD9])
                        break
                    # RSTn
                    # elif byte == 0xD0 or 0xD1 or 0xD2 or 0xD3 or 0xD4 or 0xD5 or 0xD6 or 0xD7:
                    #     segments.append(segment)
                    #     segment = []
                    else:
                        segments.append(segment)
                        segment = [byte]
        return segments
    def _read_file(path: str):
        with open(path, 'rb') as f:
            content = f.read()
        segments = Jpeg._read_segments(content)
        return segments
    def __init__(self, path: str) -> None:
        segments = Jpeg._read_file(path)
        # 判断文件完整性
        SOI(segments[0])
        EOI(segments[-1])
        # 读取图片参数
        for seg in segments[1: -1]:
            if seg[0] == 0xE0:
                APP0(seg)
            elif seg[0] == 0xC0:
                SOF0(seg)
            elif seg[0] == 0xC2:
                SOF2(seg)
            elif seg[0] == 0xC4:
                # 哈夫曼表可以重复出现（一般出现4次）
                DHT(seg)
            elif seg[0] == 0xDB:
                DQT(seg)
            elif seg[0] == 0xDD:
                DRI(seg)
            elif seg[0] == 0xFE:
                COM(seg)
            elif seg[0] == 0xDA:
                SOS(seg)
                break
            else:
                print('===== Unknown Segment:', hex(seg[0]), '=====')
        # 读取文件数据
        # for seg in segments:
        #     print(hex(seg[0]), len(seg))
        # print(len(segments))


if __name__ == '__main__':
    jpeg = Jpeg(f'./img/suey.jpg')

