import random


class PBox:

    def __init__(self, perm_key=None):
        self.perm_key = perm_key
        if not perm_key:
            self.generate_perm_key()

    def permutation(self, bit_string):
        new_bit_string = ['a' for i in range(16)]
        for index, bit in enumerate(bit_string):
            new_pos = self.perm_key[index] - 1  # -1 as 0-index in python
            new_bit_string[new_pos] = bit

        return ''.join(new_bit_string)

    def generate_perm_key(self):
        """Generate random permutation from S_16"""
        values = [i for i in range(16)]
        random.shuffle(values)

        self.perm_key = values

    def set_key(self, key):
        """Set the key to be a predefined value"""
        self.perm_key = key
