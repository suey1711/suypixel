from struct import pack
from enum import Enum
import PIL.Image
from io import BufferedWriter

def write_soi(f: BufferedWriter):
    f.write(pack(">H", 0xffd8))

def write_app0(f: BufferedWriter):
    f.write(pack(">H", 0xffe0))
    f.write(pack(">H", 16))
    f.write(pack(">L", 'JFIF'))
    f.write(pack(">B", 0))
    f.write(pack(">H", 0x0101)) # 版本号：1.1
    f.write(pack(">I", 0x0048))   # X方向像素密度
    f.write(pack(">I", 0x0048))   # Y方向像素密度
    f.write(pack(">H", 0x0000)) # 无缩略图

def write_dqt0(f: BufferedWriter):
    f.write(pack(">H", 0xffdb))

def write_dqt1(f: BufferedWriter):
    f.write(pack(">H", 0xffdb))

def write_sof0(f: BufferedWriter):
    f.write(pack(">H", 0xffc0))

def write_dht_dc0(f: BufferedWriter):
    f.write(pack(">H", 0xffc4))

def write_dht_ac0(f: BufferedWriter):
    f.write(pack(">H", 0xffc4))

def write_dht_dc1(f: BufferedWriter):
    f.write(pack(">H", 0xffc4))

def write_dht_ac1(f: BufferedWriter):
    f.write(pack(">H", 0xffc4))

def write_sos(f: BufferedWriter):
    f.write(pack(">H", 0xffda))

def write_header(f: BufferedWriter):
    write_soi(f)
    write_app0(f)
    write_dqt0(f)
    write_dqt1(f)
    write_sof0(f)
    write_dht_dc0(f)
    write_dht_ac0(f)
    write_dht_dc1(f)
    write_dht_ac1(f)
    write_sos(f)

def write_data(f: BufferedWriter, biWidth, biHeight):
    pass

def write_file(path: str):
    with open(path, 'wb') as f:
        write_header(f)
        write_data(f)

if __name__ == '__main__':
    # write_file(r'./test.jpeg')
    pass