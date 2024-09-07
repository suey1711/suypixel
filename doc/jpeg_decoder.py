def read_file(path: str):

    with open(path, 'rb') as f:
        content = f.read()

    segments = []
    segment = []
    flag = False
    i = 0
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
                    print(hex(byte))
                    segments.append(segment)
                    segment = [byte]

    print(len(segments))

if __name__ == '__main__':
    read_file(f'./img/suey.jpeg')