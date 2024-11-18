import numpy as np
from Utils import *
from Key_Expansion import *


def add_round_key(state, round_key):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]
    return state


def sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = Sbox[state[i][j]]
    return state


def shift_rows(state):
    state[1][0], state[1][1], state[1][2], state[1][3] = \
        state[1][1], state[1][2], state[1][3], state[1][0]
    state[2][0], state[2][1], state[2][2], state[2][3] = \
        state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = \
        state[3][3], state[3][0], state[3][1], state[3][2]
    return state


def mix_columns(state):
    new_state = []
    for col in range(4):
        new_column = []
        for row in range(4):
            val = 0
            for i in range(4):
                val ^= gf2_multiply_and_reduce(
                    MIxColMatrix[row][i], state[i][col])
            new_column.append(val)
        new_state.append(new_column)
    new_state = transpose_key(new_state)
    return new_state


def two_round_aes(message, initial_key):
    mid_states = {}
    round_keys = generate_round_keys(initial_key)
    K0, K1, K2 = round_keys[0], round_keys[1], round_keys[2]

    # state = message_to_matrix(message)
    state = message
    mid_states["Message                 : "] = state_matrix_to_hex(state)
    state = add_round_key(state, K0)
    mid_states["Round Key Apply         : "] = state_matrix_to_hex(state)

    # First Round
    state = sub_bytes(state)
    mid_states["First Round Sub         : "] = state_matrix_to_hex(state)
    state = shift_rows(state)
    mid_states["First Round Shift       : "] = state_matrix_to_hex(state)
    state = mix_columns(state)
    mid_states["First Round Mix Col     : "] = state_matrix_to_hex(state)
    state = add_round_key(state, K1)
    mid_states["First Round Key Apply   : "] = state_matrix_to_hex(state)

    # Second Round
    state = sub_bytes(state)
    mid_states["Second Round Sub        : "] = state_matrix_to_hex(state)
    state = shift_rows(state)
    mid_states["Second Round Shift      : "] = state_matrix_to_hex(state)
    state = add_round_key(state, K2)
    mid_states["Second Round Key Apply  : "] = state_matrix_to_hex(state)

    # Convert state matrix back to 128-bit array
    ciphertext = state_matrix_to_hex(state)
    mid_states["CipherText              : "] = state_matrix_to_hex(state)

    return ciphertext, mid_states


def main():
    for i in range(4):
        for j in range(4):
            message_pairs = give_message_pairs(i, j)
            cipher1, mid_state1 = two_round_aes(message_pairs[0], initial_key)
            cipher2, mid_state2 = two_round_aes(message_pairs[1], initial_key)
            print(f"location {i},{j}\n")
            print("Message 1 : ", state_matrix_to_hex(message_pairs[0]))
            print("Message 2 : ", state_matrix_to_hex(message_pairs[1]))
            print("Cipher  1 : ", cipher1)
            print("Cipher  2 : ", cipher2)

            print("\nXor Variation\n")
            xor_dicts(mid_state1, mid_state2)
            print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
