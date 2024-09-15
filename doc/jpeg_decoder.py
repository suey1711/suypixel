# 缩写	字节码	名称	注释
# SOI	0xFFD8	Start of image 文件开头
# SOF0	0xFFC0	Start of Frame0 Baseline DCT-based JPEG所用的开头
# SOF2	0xFFC2	Start of Frame2 Progressive DCT-based JPEG
# DHT	0xFFC4	Define Huffman Tables 指定一个或多个哈夫曼表
# DQT	0xFFDB	Define Quantization Table 指定量化表
# DRI	0xFFDD	Define Restart Interval ST中的marker
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
    pass

class SOF2:
    'Start of Frame2 Progressive DCT-based JPEG'
    pass

class DHT:
    'Define Huffman Tables'
    pass

class DQT:
    'Define Quantization Table'
    pass

class DRI:
    'Define Restart Interval ST中的marker'
    pass

class SOS:
    'Start of Scan'
    pass

class Frame:
    pass

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
        # 读取文件数据
        # for seg in segments:
        #     print(hex(seg[0]), len(seg))
        # print(len(segments))


if __name__ == '__main__':
    jpeg = Jpeg(f'./img/suey.jpg')

