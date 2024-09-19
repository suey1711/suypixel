# 缩写	字节码	名称	注释
# SOI	0xFFD8	Start of image 文件开头
# SOF0	0xFFC0	Baseline DCT-based JPEG
# SOF2	0xFFC2	Progressive DCT-based JPEG
# DHT	0xFFC4	Define Huffman Tables
# DQT	0xFFDB	Define Quantization Table
# DRI	0xFFDD	Define Restart Interval RST中的marker
# SOS	0xFFDA	Start of Scan Scan的开头
# RSTn	0xFFDn	Restart DRImarker中插入r个块
# APPn	0xFFEn	Application-specific Exif JPEG使用APP1, JFIF JPEG使用APP0
# COM	0xFFFE	Comment 注释内容
# EOI	0xFFD9	End of Image 图像的结束

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

class SOF0:
    'Start of Frame0 Baseline DCT-based JPEG'
    # 标记代码｜｜  2 bytes 固定值：0xFFC0
    # 数据长度｜｜  2 bytes 包含自身但不包含标记代码
    # 精度｜｜｜｜  1 byte  每个样本数据的位数，通常是8位
    # 图像高度｜｜  2 bytes 单位：像素
    # 图像宽度｜｜  2 bytes 单位：像素
    # 颜色分量数｜  2 bytes 灰度级1，YCbCr或YIQ是3，CMYK是4
    # 颜色分量信息  颜色分量数 * 3 bytes
    #       1 byte 分量ID
    #       1 byte 采样因子（前4位：水平采样，后4位：垂直采样）
    #       1 byte 当前分量使用的量化表ID
    def __init__(self, segment: bytes) -> None:
        print('SOF0 Len:', len(segment))

class SOF2:
    'Start of Frame2 Progressive DCT-based JPEG'
    def __init__(self, segment: bytes) -> None:
        print('SOF2 Len:', len(segment))

class DHT:
    'Define Huffman Tables'
    # 标记代码｜｜  2 bytes 固定值：0xFFC0
    # 数据长度｜｜  2 bytes 包含自身但不包含标记代码
    # 哈夫曼表｜｜  (length - 2) bytes
    #       表ID和表类型  1 byte
    #       	高4位：类型，只有两个值可选，0为DC直流，1为AC交流
    #           低4位：哈夫曼表ID，注意DC表和AC表是分开编码的
    #       不同位数的码字数量 16 bytes
    #       编码内容  上述16个不同位数的码字的数量和 bytes
    def __init__(self, segment: bytes) -> None:
        print('DHT Len:', len(segment))

class DQT:
    'Define Quantization Table'
    # 标记代码｜｜  2 bytes 固定值：0xFFC0
    # 数据长度｜｜  2 bytes 包含自身但不包含标记代码
    # 量化表｜｜｜  （length - 2） bytes
    #       精度和ID  1 byte
    #               高4位为精度，只有两个可选值：0表示8bits，1表示16bits
    #               低4位为量化表ID，取值范围为0~3
    #       表项  64 * (精度 + 1)bytes
    def __init__(self, segment: bytes) -> None:
        print('DQT Len:', len(segment))

class DRI:
    'Define Restart Interval ST中的marker'
    def __init__(self, segment: bytes) -> None:
        print('DRI Len:', len(segment))

class SOS:
    'Start of Scan'
    # 标记代码｜｜  2 bytes 固定值：0xFFDA
    # 数据长度｜｜  2 bytes 包含自身但不包含标记代码
    # 颜色分量数｜  2 bytes 灰度级1，YCbCr或YIQ是3，CMYK是4
    # 颜色分量信息  颜色分量数 * 3 bytes
    #       1 byte 分量ID
    #       1 byte 采样因子（前4位：水平采样，后4位：垂直采样）
    #       1 byte 当前分量使用的量化表ID
    # 压缩图像信息  3bytes
    #       1 byte 谱选择开始 固定为0x00
    #       1 byte 谱选择结束 固定为0x3f
    #       1 byte 谱选择 在basic JPEG中固定为00
    def __init__(self, segment: bytes) -> None:
        print('SOS Len:', len(segment))

class COM:
    'Comment'
    def __init__(self, segment: bytes) -> None:
        print('COM Len:', len(segment))

class APP0:
    'Application-specific 0'
    # 标记代码｜｜  2 bytes 固定值：0xFFE0
    # 数据长度｜｜  2 bytes 包含自身但不包含标记代码
    # 标识符｜｜｜  5 bytes Identifier 固定长度字符串："JFIF\0"
    # 版本号｜｜｜  2 bytes 一般为0x0101或0x0102，表示1.1或1.2
    # 像素单位｜｜  1 byte  坐标单位
    #       0 没有单位
    #       1 pixel/inch
    #       2 pixel/inch
    # 水平像素数目  2 bytes
    # 垂直像素数目  2 bytes
    # 缩略图素数目  2 bytes
    #       1 byte 水平
    #       1 byte 垂直
    # 缩略图位图 3n bytes
    # n = 缩略图水平像素数目*缩略图垂直像素数目
    # 这是一个24bits/pixel的RGB位图
    def __init__(self, segment: bytes) -> None:
        print('APP0 Len:', len(segment))

class APPn:
    'Application-specific n'
    # 标记代码｜｜  2 bytes 固定值：0xFFE0
    # 数据长度｜｜  2 bytes 包含自身但不包含标记代码
    # 详细信息｜｜  (length - 2) bytes
    #       Exif使用APP1来存放图片的metadata
    #       Adobe Photoshop用APP1和APP13两个标记段分别存储了一副图像的副本
    def __init__(self, segment: bytes) -> None:
        print('APP0 Len:', len(segment))

class Jpeg(SOI, EOI, SOF0, SOF2, DHT, DQT, DRI):
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
        SOI.__init__(self, segments[0])
        EOI.__init__(self, segments[-1])
        # 读取图片参数
        for seg in segments[1: -1]:
            if seg[0] == 0xC0:
                SOF0.__init__(self, seg)
            elif seg[0] == 0xC2:
                SOF2.__init__(self, seg)
            elif seg[0] == 0xC4:
                # 哈夫曼表可以重复出现（一般出现4次）
                DHT.__init__(self, seg)
            elif seg[0] == 0xDB:
                DQT.__init__(self, seg)
            elif seg[0] == 0xDD:
                DRI.__init__(self, seg)
            elif seg[0] == 0xDA:
                SOS.__init__(self, seg)
            elif seg[0] == 0xFE:
                SOS.__init__(self, seg)
            else:
                print('Unknown Segment:', hex(seg[0]))
        # 读取文件数据
        # for seg in segments:
        #     print(hex(seg[0]), len(seg))
        # print(len(segments))


if __name__ == '__main__':
    jpeg = Jpeg(f'./img/suey.jpg')

