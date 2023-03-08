import collections

from src.spn.SBox import SBox
from src.spn.PBox import PBox
from src.utility.utility import xor, int2nibble, nibble2int, break2nibbles


def generate_difference_distribution(sbox, nibbles):
    table = []
    for nibble in nibbles:
        row = generate_difference_distribution_row(sbox, nibbles, nibble)
        table.append(row)
    return table


def generate_difference_distribution_row(sbox, nibbles, diff):
    # Generate list of pairs with the desired difference
    target_pairs = []
    for nibble in nibbles:
        target_pairs.append([nibble, xor(nibble, diff)])

    # Push each pair through S-box and store result
    pair_substitution_result = []
    for pair in target_pairs:
        pair_substitution_result.append([sbox.substitution(pair[0]), sbox.substitution(pair[1])])

    # List of observed differences to calculate frequencies
    obs_diffs = []
    for pair in pair_substitution_result:
        obs_diffs.append(xor(pair[0], pair[1]))

    # Count frequencies
    frequencies = dict.fromkeys(nibbles, 0)
    for obs_diff in obs_diffs:
        frequencies[obs_diff] += 1

    return list(frequencies.values())


def get_propagation_ratio(table, state, pbox):
    probability = 1

    # For the first 3 rounds
    for r in range(3):  # TODO: Loop over list of pboxes
        # Split 16 bit start into 4x4 bit strings
        state = break2nibbles(state)

        # For each nibble in state, find the most likely result after substitution
        for pos, nibble in enumerate(state):
            difference_distribution_row = table[nibble2int(nibble)]

            if nibble == '0000':  # '0000' always maps to '0000'
                _max = 16
                most_likely = '0000'
            else:  # Find nibble most likely to occur (finding the position of the maximum element)
                _max = 0
                max_idx = 0
                for i, occurrence in enumerate(difference_distribution_row):
                    if occurrence > _max:
                        _max = occurrence
                        max_idx = i

                most_likely = int2nibble(max_idx)

            probability *= _max / 16  # Update probability of this substitution
            state[pos] = most_likely  # Update state with the most likely substitution

        # Perform the permutation
        state = pbox.permutation(''.join(state))

    return probability


def find_differential_trail(candidate_starts, table, pbox):
    ratios = {}
    # Generate possible starting states
    for nibble in candidate_starts:
        print("*"*40)
        print("Starting Nibble:", nibble)
        for i in range(3):
            state = break2nibbles('0000000000000000')
            state[i] = nibble
            state = ''.join(state)
            prop_ratio = get_propagation_ratio(table, state, pbox)

            print("State:", state)
            print("Propagation Ratio:", prop_ratio)
            ratios[state] = prop_ratio

    return ratios


if __name__ == "__main__":
    sub_key = {'0': '7', '1': 'd', '2': 'e', '3': '3', '4': '0', '5': '6', '6': '9', '7': 'a', '8': '1', '9': '2',
               'a': '8', 'b': '5', 'c': 'b', 'd': 'c', 'e': '4', 'f': 'f'
               }
    sbox = SBox(sub_key)

    perm_key = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]
    pbox = PBox(perm_key)

    # Generate list of nibbles to use
    nibbles = [bin(i)[2:].zfill(4) for i in range(16)]

    # Calculate entire difference distribution table
    table = generate_difference_distribution(sbox, nibbles)
    for row in table:
        print(row)

    # Find differential trails with high propagation ratios
    # The starting keys are the nibbles that have 6/16 chance of being transformed to another bit - nibbles that
    # have '6' in their row of the difference distribution table
    candidate_starts = ['0010', '0011', '1000', '1011', '1100', '1110']
    ratios = find_differential_trail(candidate_starts, table, pbox)


