from utils import *

s_box = [6, 4, 12, 5, 0, 7, 2, 14, 1, 15, 3, 13, 8, 10, 9, 11]

inverse_s_box = [0] * len(s_box)
for i, value in enumerate(s_box):
    inverse_s_box[value] = i

p_box = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
inverse_p_box = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]


def sypher004_encrypt(message, keys):
    curr_input = message
    for i in range(4):
        round_input = curr_input ^ keys[i]
        round_input_parts = [(round_input >> (4 * j)) & 15 for j in range(4)]
        sbox_output_parts = [s_box[nibble] for nibble in round_input_parts]
        sbox_output = sum((sbox_output_parts[j] << (4 * j)) for j in range(4))
        curr_input = apply_permutation(sbox_output, p_box)

    round_input = curr_input ^ keys[4]
    round_input_parts = [(round_input >> (4 * j)) & 15 for j in range(4)]
    sbox_output_parts = [s_box[nibble] for nibble in round_input_parts]
    sbox_output = sum((sbox_output_parts[j] << (4 * j)) for j in range(4))
    ciphertext = sbox_output ^ keys[5]
    return ciphertext


def sypher004_decrypt(ciphertext: int, keys: list[int]) -> int:
    curr_input = ciphertext ^ keys[5]
    curr_input_parts = [(curr_input >> (4 * j)) & 15 for j in range(4)]
    sbox_output_parts = [inverse_s_box[nibble] for nibble in curr_input_parts]
    curr_input = sum((sbox_output_parts[j] << (4 * j)) for j in range(4))
    curr_input ^= keys[4]
    for i in range(3, -1, -1):
        curr_input = apply_permutation(curr_input, inverse_p_box)
        curr_input_parts = [(curr_input >> (4 * j)) & 15 for j in range(4)]
        sbox_output_parts = [inverse_s_box[nibble]
                             for nibble in curr_input_parts]
        curr_input = sum((sbox_output_parts[j] << (4 * j)) for j in range(4))
        curr_input ^= keys[i]
    plaintext = curr_input
    return plaintext


