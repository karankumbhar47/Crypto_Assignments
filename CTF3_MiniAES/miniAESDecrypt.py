from utils import *


def decrypt(ciphertext, key):
    round_keys = generate_round_keys(key)
    state = apply_round_key(ciphertext, [round_keys[5][0][0]]+[round_keys[5][1][0]]+[round_keys[5][0][1]]+[round_keys[5][1][1]])

    for i in range(5, 0, -1):
        state = reverse_row_shift(state)
        state = inverse_substitute(state)
        state = apply_round_key(state, [round_keys[i-1][0][0]]+[round_keys[i-1][1][0]]+[round_keys[i-1][0][1]]+[round_keys[i-1][1][1]])

        if i > 1:
            state = inv_mix_columns(state)

    return state
