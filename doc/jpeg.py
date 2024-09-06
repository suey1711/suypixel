from struct import unpack
from enum import Enum
import PIL.Image

def read_header(f):
    pass

def read_info(f):
    pass

def read_data(f, biWidth, biHeight):
    pass

def read_file(path: str):
    with open(path, 'rb') as f:
        pass

if __name__ == '__main__':
    pixels, biWidth, biHeight = read_file(f'./img/suey.jpeg')
    # draw
    img = PIL.Image.new('RGB', (biWidth, biHeight))
    img.putdata(pixels)
    img.show()