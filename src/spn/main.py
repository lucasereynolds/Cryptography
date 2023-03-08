def read_bmp(path):
    """Read in .bmp file from path and return bmp object"""
    return

if __name__ == "__main__":
    with open("football.bmp", 'rb') as f:
        data = bytearray(f.read())

    print(data)