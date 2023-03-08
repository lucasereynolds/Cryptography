import random

from PBox import PBox
from SBox import SBox


class Round:

    def __init__(self, key, sub_key=None, perm_key=None):
        # Assign keys, if none passed, generate pseudo-randomly
        self.sub_key = sub_key
        self.perm_key = perm_key
        if not sub_key:
            self.generate_sub_key()
        if not perm_key:
            self.generate_perm_key()

        self.p_box = PBox(self.perm_key)
        self.s_boxes = [SBox(self.sub_key) for i in range(4)]
        self.key = key

    def set_key(self, key):
        """Set the key to be a predefined value"""
        self.key = key

    def key_mix(self, state):
        return self.xor(state, self.key)

    def substitute(self, state):
        # Split 16 bit state into 4x4 bit strings
        bit_strings = []
        for i in range(0, 16, 4):
            bit_strings.append(state[i:i+4])

        # Pass each bit string through each S-box
        new_bit_strings = []
        for i in range(4):
            new_bit_strings.append(self.s_boxes[i].substitution(bit_strings[i]))

        return ''.join(new_bit_strings)

    def permute(self, state):
        return self.p_box.permutation(state)

    def run(self, state):
        state = self.key_mix(state)
        state = self.substitute(state)
        state = self.permute(state)

        return state

    def generate_keys(self):
        """Function to generate keys for the S-boxes and P-boxes"""
        self.generate_perm_key()
        self.generate_sub_key()

    def generate_sub_key(self):
        """Generate random mapping from {0,1}^4 -> {0,1}^4"""
        values = [i for i in range(16)]
        targets = [i for i in range(16)]
        random.shuffle(targets)

        self.sub_key = {hex(k)[2:]: hex(v)[2:] for (k, v) in zip(values, targets)}

    def generate_perm_key(self):
        """Generate random permutation from S_16"""
        values = [i for i in range(16)]
        random.shuffle(values)

        self.perm_key = values

    @staticmethod
    def xor(a, b):
        return bin(int(a, 2) ^ int(b, 2))[2:].zfill(len(a))


class PenultimateRound(Round):

    def __init__(self, key, sub_key=None):
        # Penultimate Round has no permutation, so the permutation key is the identity permutation
        perm_identity = [i for i in range(1, 17)]
        super().__init__(key, sub_key, perm_identity)


class FinalRound(Round):

    def __init__(self, key):
        # Final Round has no permutation nor substitution, so the permutation key and substitution are the identity

        # Construct identity keys
        values = [hex(i)[2:] for i in range(16)]
        sub_identity = {k: v for (k, v) in zip(values, values)}

        perm_identity = [i for i in range(1, 17)]

        super().__init__(key, sub_identity, perm_identity)
