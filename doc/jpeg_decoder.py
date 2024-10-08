# Jpeg Segments
# Abbr  Marker  Name                        Describe
#   ----- 非层次哈夫曼编码 -----
# SOF0  0xFFC0  Start of Frame              Baseline DCT-based
# SOF1  0xFFC1  Start of Frame              扩展顺序离散余弦变换
# SOF2  0xFFC2  Start of Frame              Progressive DCT-based
# SOF3  0xFFC3  Start of Frame              空间顺序无损
#   ----- 层次哈夫曼编码 -----
# SOF5  0xFFC5  Start of Frame              差分离散余弦变换
# SOF6  0xFFC6  Start of Frame              差分层次离散余弦变换
# SOF7  0xFFC7  Start of Frame              差分空间无损
#   ----- 非层次算术编码 -----
# SOF8  0xFFC8  Start of Frame              为JPEG扩展保留
# SOF9  0xFFC9  Start of Frame              扩展顺序离散余弦变换
# SOF10 0xFFCA  Start of Frame              递进离散余弦变换
# SOF11 0xFFCB  Start of Frame              空间顺序无损
#   ----- 层次算术编码 -----
# SOF13 0xFFCD  Start of Frame              差分离散余弦变换
# SOF14 0xFFCE  Start of Frame              差分层次离散余弦变换
# SOF15 0xFFCF  Start of Frame              差分空间无损
#   ----- - -----
# DHT   0xFFC4  Define Huffman Tables       定义哈夫曼树表
# DAC   0xFFCC  Define Arithmetic Tables    定义算数编码表
#   ----- 复位 -----
# RST0  0xFFD0  Restart                     差分编码累计复位
# RST1  0xFFD1  Restart                     差分编码累计复位
# RST2  0xFFD2  Restart                     差分编码累计复位
# RST3  0xFFD3  Restart                     差分编码累计复位
# RST4  0xFFD4  Restart                     差分编码累计复位
# RST5  0xFFD5  Restart                     差分编码累计复位
# RST6  0xFFD6  Restart                     差分编码累计复位
# RST7  0xFFD7  Restart                     差分编码累计复位
#   ----- 文件 -----
# SOI   0xFFD8  Start of Image              文件开始
# EOI   0xFFD9  End of Image                文件结束
# SOS   0xFFDA  Start of Scan               图像数据开始
#   ----- - -----
# DQT   0xFFDB  Define Quantization Table
# DNL   0xFFDC                              定义线数
# DRI   0xFFDD  Define Restart Interval     定义差分编码累计复位的间隔
# DHP   0xFFDE                              定义层次级数
# EXP   0xFFDF                              展开参考图像
#   ----- 应用程序 -----
# APP0  0xFFE0  Application Specific        JFIF JPEG
# APP1  0xFFE1  Application Specific        Exif JPEG
# ...   ...
# APP15 0xFFFD                              为应用程序保留，共15个
#   ----- JPEG -----
# JPG0  0xFFF0
# ...   ...
# JPG13 0xFFFD                              为JPEG扩展保留，共14个
#   ----- - -----
# COM   0xFFFE  Comment                     注释内容
# TEM   0xFF01                              算术编码中作临时之用
#   ----- 保留 -----
# RES   0xFF02
# ...   ...
# RES   0xFFBF                              保留，共189个

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

class APP0:
    class DensityUnit(Enum):
        Unknown = 0
        Pixel_Inch = 1
        Pixel_Cm = 2
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
        self.length = unpack('>H', bytes(segment[1:3]))[0]
        self.identifier = unpack('5s', bytes(segment[3:8]))
        self.version = unpack('>H', bytes(segment[8:10]))[0]
        self.unit = APP0.DensityUnit(unpack('B', bytes(segment[10:11]))[0])
        self.density_row = unpack('>H', bytes(segment[11:13]))[0]
        self.density_col = unpack('>H', bytes(segment[13:15]))[0]
        self.thumbnail_row = unpack('B', bytes(segment[15:16]))[0]
        self.thumbnail_col = unpack('B', bytes(segment[16:17]))[0]
        self.thumbnail = segment[17:]
        if len(self.thumbnail) != self.thumbnail_row * self.thumbnail_col * 3:
            raise ValueError('thumbnail Length Error')
        if self.length != 16 + len(self.thumbnail):
            raise ValueError(f'APP0 Length Error, Expect({self.length}), Read({16 + len(self.thumbnail)})')

    def print(self):
        print(f'===== APP0 =====')
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
        self.length = unpack('>H', bytes(segment[1:3]))[0]
        self.degree = unpack('B', bytes(segment[3:4]))[0]
        self.height = unpack('>H', bytes(segment[4:6]))[0]
        self.width = unpack('>H', bytes(segment[6:8]))[0]
        self.vector_count = unpack('B', bytes(segment[8:9]))[0]
        self.dqt_map = []
        self.factor = []
        for count in range(self.vector_count):
            vector_id = segment[9 + count * 3]
            sample_factor = segment[10 + count * 3]
            vertical_factor = sample_factor & 0x0F
            horizontal_factor = sample_factor >> 4
            dqt_id = segment[11 + count * 3]
            self.dqt_map.append((vector_id, dqt_id))
            self.factor.append((vector_id, horizontal_factor, vertical_factor))
        if self.length != 11 + (self.vector_count - 1) * 3:
            raise ValueError(f'SOF0 Length Error, Expect({self.length}), Read({(self.vector_count - 1) * 3})')

    def print(self):
        print(f'===== SOF0 =====')
        print('Sample Degree:', self.degree)
        print('Image Width x Heigth:', self.height, self.width)
        print('Table ID: (Vector ID, DQT ID)')
        for vector in self.dqt_map:
            print(vector)
        print('Table ID: (Vector ID, Horizontal Factor, Vertical Factor)')
        for vector in self.factor:
            print(vector)

class DHT:
    class TableType(Enum):
        DC = 0
        AC = 1
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
        self.length = unpack('>H', bytes(segment[1:3]))[0]
        value = unpack('B', bytes(segment[3:4]))[0]
        self.id = value & 0x0F
        self.table_type = DHT.TableType(value >> 4)
        self.counts = segment[4:20]
        self.weights = []
        self.code_lens = []
        code_len = 1
        for count in self.counts:
            current_len = len(self.code_lens)
            self.weights += segment[20 + current_len: 20 + current_len + count]
            for _ in range(count):
                self.code_lens.append(code_len)
            code_len += 1

        if self.length != 19 + len(self.code_lens):
            raise ValueError(f'DHT Length Error, Expect({self.length}), Read({19 + len(self.code_lens)})')
        self.codes = DHT.generate_codes(self.counts)
        self.table = []
        for index in range(len(self.code_lens)):
            self.table.append((index, self.code_lens[index], self.codes[index], self.weights[index]))

    def generate_codes(counts: list) -> list:
        deep = 0
        cur = 0
        codes = []
        for count in counts:
            deep += 1
            for _ in range(count):
                # start
                if codes == []:
                    code = '0'
                else:
                    code = bin(int(codes[cur - 1], 2) + 1)[2:]
                    for _ in range(len(codes[cur - 1]) - len(code)):
                        code = '0' + code
                for _ in range(deep - len(code)):
                    code += '0'
                codes.append(code)
                cur += 1
        return codes

    def print(self):
        print(f'===== DHT =====')
        print(f'DHT ID: {self.id}, Type: {self.table_type}, Counts: {len(self.code_lens)}')
    def print_table(self):
        print('====', self.counts)
        for index in range(len(self.code_lens)):
            print(index, self.code_lens[index], self.codes[index], self.weights[index])

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
        self.length = unpack('>H', bytes(segment[1:3]))[0]
        value = unpack('B', bytes(segment[3:4]))[0]
        self.id = value & 0x0F
        self.degree = QuantizationDegree(value >> 4)
        self.table = segment[4:4 + 64 * (self.degree.value + 1)]
        if self.length != 3 + len(self.table):
            raise ValueError(f'DQT Length Error, Expect({self.length}), Read({3 + len(self.table)})')

    def print(self):
        print(f'===== DQT =====')
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
        self.length = unpack('>H', bytes(segment[1:3]))[0]
        self.interval = unpack('>H', bytes(segment[3:5]))[0]
        if self.length != 4:
            raise ValueError(f'DRI Length Error, Expect({self.length}), Read(4)')

    def print(self):
        print(f'===== DRI =====')
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
        self.length = unpack('>H', bytes(segment[1:3]))[0]
        self.vector_count = unpack('B', bytes(segment[3:4]))[0]
        self.dht_map = []
        for count in range(self.vector_count):
            vector_id = segment[4 + count * 2]
            dht_id = segment[5 + count * 2]
            ac = dht_id & 0x0F
            dc = dht_id >> 4
            self.dht_map.append((vector_id, dc, ac))
        self.thumbnail_spectrum_start = segment[4 + self.vector_count * 2]
        self.thumbnail_spectrum_end = segment[5 + self.vector_count * 2]
        self.thumbnail_spectrum_select = segment[6 + self.vector_count * 2]
        if self.thumbnail_spectrum_start != 0x00 \
            or self.thumbnail_spectrum_end != 0x3F:
                raise ValueError('Thumbnail Spectrum Error')
        if self.length != 6 + self.vector_count * 2:
            raise ValueError(f'SOS Length Error, Expect({self.length}), Read({6 + self.vector_count * 2})')

    def print(self):
        print(f'===== SOS =====')
        print('Thumbnail Spectrum Select:', self.thumbnail_spectrum_select)
        print('Table ID: (Vector ID, DC, AC)')
        for vector in self.dht_map:
            print(vector)

class COM:
    'Comment'
    def __init__(self, segment: bytes) -> None:
        print('COM Len:', len(segment))

class Frame:
    def __init__(self) -> None:
        self.data = []
        self.units = []
        self.huffman_table_direct = []
        self.huffman_table_alternate = []
    def append(self, data):
        self.data.append(data)
    def add_huffman_table_direct(self, table: list):
        self.huffman_table_direct.append(table)
    def add_huffman_table_alternate(self, table: list):
        self.huffman_table_alternate.append(table)
    def config(self, width, height, factor, dqt_map, dht_map):
        self.width = width
        self.height = height
        self.factor = factor
        self.dqt_map = dqt_map
        self.dht_map = dht_map

    def current_vector_index(self):
        # Get Vector Index
        if self.factor == [(1, 2, 2), (2, 1, 1), (3, 1, 1)]:
            match len(self.units) % 6:
                case 5:
                    index = 2
                case 4:
                    index = 1
                case _:
                    index = 0

        elif self.factor == [(1, 1, 1), (2, 1, 1), (3, 1, 1)]:
            index = len(self.units) % 3
        else:
            raise ValueError('Decode Huffman Error, Unknown Vector Factor')
        return index

    def push_unit(self, unit):
        self.units.append(unit)

    def decode_huffman(self):
        print(f'Frame Counts: {len(self.data)}')
        print('=== DHT MAP ===\n(ID, DC, AC)')
        print(self.factor)

        class State(Enum):
            DCCode = 0
            DCData = 1
            ACCode = 2
            ACData = 3
        # 直流哈夫曼表权值（共8位）：
        #   表示该直流分量值的二进制位数，也就是接下来需要读入的位数。
        # 交流哈夫曼表权值（共8位）：
        #   高4位表示当前数值前面有多少个连续的零
        #   低4位表示该交流分量数值的二进制位数
        for segment in self.data:
            data_unit = []
            state = State.DCCode
            code = ''
            width = 0
            length = 0
            data = 0
            dc_base = 0
            for byte in segment:
                for offset in range(8):
                    value = (byte >> (7 - offset)) & 0x01
                    match state:
                        case State.DCCode:
                            code += str(value)
                            if len(code) > 16:
                                raise ValueError('Decode Huffman Error, ReadCode Length > 16')
                            current = self.current_vector_index()
                            huffman_table = self.huffman_table_direct[self.dht_map[current][1]]
                            for huffman_entry in huffman_table:
                                if code == huffman_entry[2]:
                                    width = huffman_entry[3]
                                    if width == 0:
                                        data_unit.append(dc_base)
                                        state = State.ACCode
                                        code = ''
                                    else:
                                        state = State.DCData
                                        length = 0
                                        data = 0
                                    break
                        case State.DCData:
                            data = (data << 1) | value
                            length += 1
                            if length >= width:
                                if (data & (0x01 << (width - 1))) == 0:
                                    data = - (data | (0x01 << (width - 1)))
                                dc_base += data
                                data_unit.append(dc_base)
                                state = State.ACCode
                                code = ''
                        case State.ACCode:
                            code += str(value)
                            if len(code) > 16:
                                raise ValueError('Decode Huffman Error, ReadCode Length > 16')
                            current = self.current_vector_index()
                            huffman_table = self.huffman_table_alternate[self.dht_map[current][2]]
                            for huffman_entry in huffman_table:
                                if code == huffman_entry[2]:
                                    if huffman_entry[3] == 0:
                                        for _ in range(64 - len(data_unit)):
                                            data_unit.append(0)
                                        self.push_unit(data_unit)
                                        state = State.DCCode
                                        data_unit = []
                                        code = ''
                                    else:
                                        width = huffman_entry[3] & 0x0F
                                        pad = huffman_entry[3] >> 4
                                        for _ in range(pad):
                                            data_unit.append(0)
                                        if width == 0:
                                            data_unit.append(0)
                                            state = State.ACCode
                                            code = ''
                                        else:
                                            state = State.ACData
                                            length = 0
                                            data = 0

                                        if len(data_unit) > 64:
                                            raise ValueError('DataUnit Length > 64 ACCode')
                                        elif len(data_unit) == 64:
                                            self.push_unit(data_unit)
                                            state = State.DCCode
                                            data_unit = []
                                            code = ''
                                    break
                        case State.ACData:
                            data = (data << 1) | value
                            length += 1
                            if length >= width:
                                if (data & (0x01 << (width - 1))) == 0:
                                    data = - (data | (0x01 << (width - 1)))
                                data_unit.append(data)
                                state = State.ACCode
                                code = ''

                                if len(data_unit) > 64:
                                    raise ValueError('DataUnit Length > 64 ACData')
                                elif len(data_unit) == 64:
                                    self.push_unit(data_unit)
                                    state = State.DCCode
                                    data_unit = []
                                    code = ''

    def decode_quantization(self):
        pass

class Jpeg:
    def read_segments(content: bytes):
        segments = []
        segment = []
        flag = False
        for byte in content:
            # split
            if byte == 0xFF:
                flag = True
                continue
            # parse
            if flag is False:
                segment.append(byte)
            else:
                flag = False
                if byte == 0x00:
                    segment.append(0xFF)
                elif byte == 0xD8:
                    segment = [0xD8]
                elif byte == 0xD9:
                    segments.append(segment)
                    segments.append([0xD9])
                    break
                else:
                    segments.append(segment)
                    segment = [byte]
        return segments
    def _parse_segments(self, segments: list):
        self.dht_list: list[DHT] = []
        self.dqt_list: list[DQT] = []
        SOI(segments[0])
        EOI(segments[-1])
        for seg in segments[1: -1]:
            if seg[0] == 0xE0:
                self.app0 = APP0(seg)
            elif seg[0] == 0xC0:
                self.sof0 = SOF0(seg)
            elif seg[0] == 0xC4:
                # 哈夫曼表可以重复出现（一般出现4次）
                self.dht_list.append(DHT(seg))
            elif seg[0] == 0xDB:
                self.dqt_list.append(DQT(seg))
            elif seg[0] == 0xDD:
                self.dri = DRI(seg)
            elif seg[0] == 0xFE:
                self.com = COM(seg)
            elif seg[0] == 0xDA:
                self.sos = SOS(seg)
                self.frame.append(seg[1 + self.sos.length:])
            elif seg[0] == 0xD0 \
                    or seg[0] == 0xD1 \
                    or seg[0] == 0xD2 \
                    or seg[0] == 0xD3 \
                    or seg[0] == 0xD4 \
                    or seg[0] == 0xD5 \
                    or seg[0] == 0xD6 \
                    or seg[0] == 0xD7:
                self.frame.append(seg[1:])
            else:
                print('===== Unknown Segment:', hex(seg[0]), '=====')

    def __init__(self, path: str) -> None:
        self.frame = Frame()
        with open(path, 'rb') as f:
            content = f.read()
        segments = Jpeg.read_segments(content)
        self._parse_segments(segments)
        self.frame.config(self.sof0.width, self.sof0.height
                          , self.sof0.factor
                          , self.sof0.dqt_map
                          , self.sos.dht_map)
        for dht in self.dht_list:
            if dht.table_type is DHT.TableType.DC:
                self.frame.add_huffman_table_direct(dht.table)
            else:
                self.frame.add_huffman_table_alternate(dht.table)
        # Decode
        # huffman and diff
        self.frame.decode_huffman()
        # zig-zag
        self.frame.decode_quantization()
        # IDCT
        # YCrCb to RGB


if __name__ == '__main__':
    jpeg = Jpeg(f'./img/suy.jpg')

