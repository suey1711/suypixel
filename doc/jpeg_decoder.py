# 缩写	字节码	名称	注释
# SOI	0xFFD8	Start of image	文件开头
# SOF0	0xFFC0	Start of Frame0	Baseline DCT-based JPEG所用的开头
# SOF2	0xFFC2	Start of Frame2	Progressive DCT-based JPEG
# DHT	0xFFC4	Define Huffman Tables	指定一个或多个哈夫曼表
# DQT	0xFFDB	Define Quantization Table	指定量化表
# DRI	0xFFDD	Define Restart Interval	RST中的marker
# SOS	0xFFDA	Start of Scan	Scan的开头
# RSTn	0xFFDn	Restart	DRImarker中插入r个块
# APPn	0xFFEn	Application-specific	Exif JPEG使用APP1，JFIF JPEG使用APP0
# COM	0xFFFE	Comment	注释内容
# EOI	0xFFD9	End of Image	图像的结束
def read_file(path: str):
    with open(path, 'rb') as f:
        content = f.read()

    segments = []
    segment = [0xFF]
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
                else:
                    segments.append(segment)
                    segment = [byte]

    for seg in segments:
        print(hex(seg[0]), len(seg))
    print(len(segments))

if __name__ == '__main__':
    read_file(f'./img/suey.jpg')