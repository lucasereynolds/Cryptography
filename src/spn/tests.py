import unittest


class TestSPN(unittest.TestCase):

    def test_SBox(self):
        from SBox import SBox
        # Set Up
        test_key = {'0': '4', '1': '1', '2': 'e', '3': '8','4': 'd', '5': '6', '6': '2', '7': 'b', '8': 'f', '9': 'c',
                    'a': '9', 'b': '7', 'c': '3', 'd': 'a', 'e': '5', 'f': '0'
                    }
        sbox = SBox(test_key)

        self.assertEqual(sbox.substitution('1100'), '0011')

    def test_PBox(self):
        from PBox import PBox
        # Set Up
        test_key = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]
        pbox = PBox(test_key)

        self.assertEqual(pbox.permutation('1001110000110010'), '1100010000111010')
    
    def test_round(self):
        from Round import Round
        # Set Up
        plaintext = '0100111010100001'
        key = '1110011101100111'
        expected_res_post_key_mix = '1010100111000110'
        expected_res_post_sub = '1001110000110010'
        expected_res_post_perm = '1100010000111010'

        sub_key = {'0': '4', '1': '1', '2': 'e', '3': '8', '4': 'd', '5': '6', '6': '2', '7': 'b', '8': 'f', '9': 'c',
                'a': '9', 'b': '7', 'c': '3', 'd': 'a', 'e': '5', 'f': '0'
                }
        perm_key = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]
        r = Round(key, sub_key, perm_key)

        self.assertEqual(r.key_mix(plaintext), expected_res_post_key_mix)
        self.assertEqual(r.substitute(expected_res_post_key_mix), expected_res_post_sub)
        self.assertEqual(r.permute(expected_res_post_sub), expected_res_post_perm)

    def test_PenultimateRound(self):
        from Round import PenultimateRound
        # Set Up
        plaintext = '0101011000101001'
        key = '0111100100000011'
        expected_res_post_key_mix = '0010111100101010'
        expected_res_post_sub = '1110000011101001'
        expected_res_post_perm = '1110000011101001'

        sub_key = {'0': '4', '1': '1', '2': 'e', '3': '8', '4': 'd', '5': '6', '6': '2', '7': 'b', '8': 'f', '9': 'c',
                   'a': '9', 'b': '7', 'c': '3', 'd': 'a', 'e': '5', 'f': '0'
                   }
        r = PenultimateRound(key, sub_key)

        self.assertEqual(r.key_mix(plaintext), expected_res_post_key_mix)
        self.assertEqual(r.substitute(expected_res_post_key_mix), expected_res_post_sub)
        self.assertEqual(r.permute(expected_res_post_sub), expected_res_post_perm)

    def test_FinalRound(self):
        from Round import FinalRound
        # Set Up
        plaintext = '1110000011101001'
        key = '1001000000111101'
        expected_res_post_key_mix = '0111000011010100'
        expected_res_post_sub = '0111000011010100'
        expected_res_post_perm = '0111000011010100'

        r = FinalRound(key)

        self.assertEqual(r.key_mix(plaintext), expected_res_post_key_mix)
        self.assertEqual(r.substitute(expected_res_post_key_mix), expected_res_post_sub)
        self.assertEqual(r.permute(expected_res_post_sub), expected_res_post_perm)

    def test_spn(self):
        from SPN import SPN
        # Set Up
        plaintext = '0100111010100001'
        keystream = '11100111011001111001000000111101'
        num_rounds = 5

        sub_key = [{'0': '4', '1': '1', '2': 'e', '3': '8', '4': 'd', '5': '6', '6': '2', '7': 'b', '8': 'f', '9': 'c',
                    'a': '9', 'b': '7', 'c': '3', 'd': 'a', 'e': '5', 'f': '0'} for i in range(num_rounds)]
        perm_key = [[1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16] for i in range(num_rounds)]
        spn = SPN(keystream, sub_key, perm_key, num_rounds)

        self.assertEqual(spn.encrypt(plaintext), '0111000011010100')


class Testps2(unittest.TestCase):

    def test_generate_difference_distribution(self):
        from src.differential_cryptanalysis import generate_difference_distribution
        from SBox import SBox
        # Set Up
        sub_key = {'0': '4', '1': '1', '2': 'e', '3': '8', '4': 'd', '5': '6', '6': '2', '7': 'b', '8': 'f', '9': 'c',
                   'a': '9', 'b': '7', 'c': '3', 'd': 'a', 'e': '5', 'f': '0'
                   }
        sbox = SBox(sub_key)

        nibbles = [bin(i)[2:].zfill(4) for i in range(16)]  # Generate list of nibbles to use
        expected_result = [[16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 2, 0, 4, 2, 0, 0, 4, 0, 2, 0, 0, 2, 0],
                           [0, 0, 0, 0, 0, 0, 4, 0, 0, 2, 4, 2, 0, 2, 0, 2],
                           [0, 0, 0, 2, 2, 2, 2, 0, 2, 0, 0, 0, 2, 0, 0, 4],
                           [0, 0, 0, 2, 0, 0, 2, 4, 0, 2, 0, 0, 6, 0, 0, 0],
                           [0, 0, 4, 0, 0, 4, 0, 0, 0, 2, 2, 0, 2, 0, 0, 2],
                           [0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 6, 0, 2, 2, 2, 0],
                           [0, 0, 0, 4, 2, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 4],
                           [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 2, 2, 2, 2],
                           [0, 2, 2, 0, 0, 2, 0, 2, 2, 2, 0, 0, 0, 0, 4, 0],
                           [0, 6, 0, 0, 2, 0, 4, 0, 2, 0, 0, 0, 0, 2, 0, 0],
                           [0, 0, 2, 4, 0, 0, 0, 2, 6, 0, 0, 0, 0, 2, 0, 0],
                           [0, 0, 2, 0, 0, 0, 0, 2, 2, 0, 2, 6, 2, 0, 0, 0],
                           [0, 2, 4, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 4, 0],
                           [0, 6, 2, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 4, 0, 0],
                           [0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 2]
                           ]

        self.assertEqual(generate_difference_distribution(sbox, nibbles), expected_result)

    def test_generate_difference_distribution_row(self):
        from src.differential_cryptanalysis import generate_difference_distribution_row
        from SBox import SBox
        # Set Up
        sub_key = {'0': '4', '1': '1', '2': 'e', '3': '8', '4': 'd', '5': '6', '6': '2', '7': 'b', '8': 'f', '9': 'c',
                   'a': '9', 'b': '7', 'c': '3', 'd': 'a', 'e': '5', 'f': '0'
                   }
        sbox = SBox(sub_key)

        nibbles = [bin(i)[2:].zfill(4) for i in range(16)]  # Generate list of nibbles to use
        diff = '1111'
        expected_result = [0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 2]

        self.assertEqual(generate_difference_distribution_row(sbox, nibbles, diff), expected_result)


if __name__ == '__main__':
    unittest.main()
