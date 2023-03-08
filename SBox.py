import random


class SBox:
    """Implementation of an S-box that performs a substitution cipher encryption on blocks of four bits"""

    def __init__(self, sub_key=None):
        self.sub_key = sub_key
        if not sub_key:
            self.generate_sub_key()

    def substitution(self, bitstring):
        """Returns mapped value of block in hex"""
        # Convert bitstring to hex
        hex_val = hex(int(bitstring, 2))[2:]

        mapped_value = self.sub_key[hex_val]

        # Return binary string from hex value, of length of bitstring
        return bin(int(mapped_value, 16))[2:].zfill(len(bitstring))

    def generate_sub_key(self):
        """Generate random mapping from {0,1}^4 -> {0,1}^4"""
        values = [i for i in range(16)]
        targets = [i for i in range(16)]
        random.shuffle(targets)

        self.sub_key = {hex(k)[2:]: hex(v)[2:] for (k, v) in zip(values, targets)}

    def set_key(self, key):
        """Set the key to be a predefined value"""
        self.sub_key = key
