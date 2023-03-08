from SPN import SPN
from utility import xor


def ecb(spn, bitstring_list):
    for idx, bitstring in enumerate(bitstring_list):
        bitstring_list[idx] = spn.encrypt(bitstring)

    return bitstring_list


def cbc(spn, bitstring_list, initial_value):
    y = initial_value
    for idx, bitstring in enumerate(bitstring_list):
        bitstring = xor(y, bitstring)
        bitstring = spn.encrypt(bitstring)
        bitstring_list[idx] = bitstring

        y = bitstring  # Change result to next y value

    return bitstring_list


def ofb(spn, bitstring_list, initial_value):
    z = initial_value

    # Create keystream
    keystream = []
    for i in range(bitstring_list):
        keystream.append(spn.encrypt(z))
    
    # Xor i-th key in keystream with i-th bitstring to encrypt
    for idx, bitstring in enumerate(bitstring_list):
        bitstring_list[idx] = xor(keystream[idx], bitstring)

    return bitstring_list


def cfb(spn, bitstring_list, initial_value):
    y = initial_value
    for idx, bitstring in enumerate(bitstring_list):
        y = xor(spn.encypt(y), bitstring)

        bitstring_list[idx] = y  # Change result to next y value

    return bitstring_list


if __name__ == "__main__":
    pass
    