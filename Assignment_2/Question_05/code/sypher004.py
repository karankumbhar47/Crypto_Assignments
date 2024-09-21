# sypher004.py
# sypher004 implementation

# s_box --> substitution box
# p_box --> permutaion box 
s_box = [6, 4, 12, 5, 0, 7, 2, 14, 1, 15, 3, 13, 8, 10, 9, 11]
p_box = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]


def apply_permutation(input_bits : int) -> int:
    """
    Applies a permutation to the input bits based on the p_box.

    @param input_bits: An integer representing the input bits to be permuted.
    @return: An integer representing the permuted output bits.
    """
    permuted_bits = 0
    for i in range(16):
        bit = (input_bits >> i) & 1
        permuted_bits |= (bit << p_box[i])
    return permuted_bits


def sypher004(message: str, keys: list[int]) -> list[int]:
    """
    Encrypts a message using the Sypher004 algorithm.

    @param message: A string representing the message to be encrypted.
    @param keys: A list of integers representing the round keys used for encryption.
    @return: A list of integers representing the outputs after each round, 
             including the final ciphertext.
    """
    roundoutputs = []
    curr_input = message

    for i in range(4):
        round_input = curr_input ^ keys[i]
        roundoutputs.append(round_input)
        round_input_parts = [(round_input >> (4 * j)) & 15 for j in range(4)]
        sbox_output_parts = [s_box[nibble] for nibble in round_input_parts]

        sbox_output = 0
        for j in range(4):
            sbox_output |= (sbox_output_parts[j] << (4 * j))

        curr_input = apply_permutation(sbox_output)

    round_input = curr_input ^ keys[4]
    roundoutputs.append(round_input)

    round_input_parts = [(round_input >> (4 * j)) & 0xf for j in range(4)]
    sbox_output_parts = [s_box[nibble] for nibble in round_input_parts]

    sbox_output = 0
    for j in range(4):
        sbox_output |= (sbox_output_parts[j] << (4 * j))

    ciphertext = sbox_output ^ keys[5]
    roundoutputs.append(ciphertext)

    return roundoutputs 
