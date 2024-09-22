# sypher004.py
# Sypher004 Implementation

# S_Box --> substitution box
# P_Box --> permutaion box 
S_Box = [6, 4, 12, 5, 0, 7, 2, 14, 1, 15, 3, 13, 8, 10, 9, 11]
P_Box = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]


def apply_permutation(input_bits : int) -> int:
    permuted_bits = 0
    for i in range(16):
        bit = (input_bits >> i) & 1
        permuted_bits |= (bit << P_Box[i])
    return permuted_bits


def Sypher004(message: str, keys: list[int]) -> list[int]:
    roundOutputs = []
    curr_input = message

    for i in range(4):
        round_input = curr_input ^ keys[i]
        roundOutputs.append(round_input)
        round_input_parts = [(round_input >> (4 * j)) & 15 for j in range(4)]
        sbox_output_parts = [S_Box[nibble] for nibble in round_input_parts]

        sbox_output = 0
        for j in range(4):
            sbox_output |= (sbox_output_parts[j] << (4 * j))

        curr_input = apply_permutation(sbox_output)

    round_input = curr_input ^ keys[4]
    roundOutputs.append(round_input)

    round_input_parts = [(round_input >> (4 * j)) & 0xf for j in range(4)]
    sbox_output_parts = [S_Box[nibble] for nibble in round_input_parts]

    sbox_output = 0
    for j in range(4):
        sbox_output |= (sbox_output_parts[j] << (4 * j))

    ciphertext = sbox_output ^ keys[5]
    roundOutputs.append(ciphertext)

    return roundOutputs 
