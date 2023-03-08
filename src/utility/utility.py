def xor(a, b):
    """
    Performs bitwise XOR operation on two-equal length bitstrings, left padding 
    the result with 0s to match the length of the bitstrings.
    """
    return bin(int(a, 2) ^ int(b, 2))[2:].zfill(len(a))


def nibble2int(nibble):
    return int(nibble, 2)


def int2nibble(integer):
    return bin(integer)[2:].zfill(4)


def break2nibbles(bitstring):
    """
    Returns list of consecutive nibbles:
    eg. '0000111100000000' -> ['0000', '1111', '0000', '0000]
    """
    n = 4
    return [bitstring[i:i + n] for i in range(0, len(bitstring), n)]


if __name__ == "__main__":
    print(nibble2int('1111'))
    print(int2nibble(10))
