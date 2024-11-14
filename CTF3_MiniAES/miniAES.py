from utils import *


def nibble_substitution(state):
    return [SUBSTITUTION_BOX[nibble] for nibble in state]

def row_shift(state):
    return [state[0], state[3], state[2], state[1]]

def mix_column(state):
    new_state = [gf_mult(state[0], 0x3) ^ gf_mult(state[1], 0x2),
        gf_mult(state[0], 0x2) ^ gf_mult(state[1], 0x3),
        gf_mult(state[2], 0x3) ^ gf_mult(state[3], 0x2),
        gf_mult(state[2], 0x2) ^ gf_mult(state[3], 0x3)]
    return new_state

def encrypt(plaintext, key):
    round_keys = generate_round_keys(key)
    state = apply_round_key(plaintext, [round_keys[0][0][0]]+[round_keys[0][1][0]]+[round_keys[0][0][1]]+[round_keys[0][1][1]])
    for i in range(5):
        state = nibble_substitution(state)
        state = row_shift(state)
        if i < 4:
            state = mix_column(state)
        state = apply_round_key(state, [round_keys[i+1][0][0]]+[round_keys[i+1][1][0]]+[round_keys[i+1][0][1]]+[round_keys[i+1][1][1]])
    return state

