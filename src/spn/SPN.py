from Round import Round, PenultimateRound, FinalRound


class SPN:

    def __init__(self, keystream, s_keys, p_keys, num_rounds):
        self.keystream = keystream
        self.s_keys = s_keys
        self.p_keys = p_keys

        # Empty initialisations - will be assigned values in `self.set_up_rounds()`
        self.rounds = []
        self.key_rounds = []

        self.set_up_rounds(num_rounds)

    def encrypt(self, plaintext):
        state = plaintext
        for r in self.rounds:
            state = r.run(state)

        return state

    def generate_key_rounds(self, num_rounds):
        """Generate key rounds from the keystream. At the moment can't wrap around."""
        key_length = 16
        start_bit = 0
        for i in range(num_rounds):
            self.key_rounds.append(self.keystream[start_bit:start_bit + key_length])
            start_bit = (start_bit + 4) % len(self.keystream)

    def set_up_rounds(self, num_rounds):
        """Set up `num_rounds` Round objects"""
        self.generate_key_rounds(num_rounds)
        for i, key in enumerate(self.key_rounds):
            sub_key = self.s_keys[i]
            perm_key = self.p_keys[i]
            if num_rounds - (i+1) == 1:  # Add Penultimate Round
                self.rounds.append(PenultimateRound(key, sub_key))
                continue
            elif (i+1) == num_rounds:  # Add final round
                self.rounds.append(FinalRound(key))
                continue
            self.rounds.append(Round(key, sub_key, perm_key))
