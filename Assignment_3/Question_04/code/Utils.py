import subprocess


def generate_128_bit_message_openssl():
    result = subprocess.run(['openssl', 'rand', '-hex', '16'],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    hex_message = result.stdout.decode().strip()
    return hex_message


def gf2_multiply_and_reduce(a_poly, b_poly):
    irreducible_poly = 0x11B
    result = 0
    temp_b = b_poly
    for i in range(8):
        if (a_poly & (1 << i)) != 0:
            result ^= temp_b
        temp_b <<= 1

    while result >= 0x100:
        shift = result.bit_length() - irreducible_poly.bit_length()
        result ^= (irreducible_poly << shift)

    return result


def hex_to_state_matrix(hex_message):
    state = [int(hex_message[i:i+2], 16)
             for i in range(0, len(hex_message), 2)]
    state_matrix = [state[i:i+4] for i in range(0, 16, 4)]
    return state_matrix


def state_matrix_to_hex(state_matrix):
    flattened_state = [byte for row in state_matrix for byte in row]
    hex_message = ''.join([f'{byte:02x}' for byte in flattened_state])
    return hex_message


def modify_byte_in_state(state_matrix, row, col, new_value):
    state_matrix[row][col] = new_value
    return state_matrix


def modify_state(hex_message, i, j, k):
    state_matrix = hex_to_state_matrix(hex_message)
    modified_state = modify_byte_in_state(state_matrix, i, j, k)
    return modified_state


def give_message_pairs(i, j):
    message = generate_128_bit_message_openssl()
    original_state = hex_to_state_matrix(message)
    modified_state = modify_state(message, i, j, 0xFF)
    return [original_state, modified_state]


def hex_diff(hex1, hex2):
    if len(hex1) != len(hex2):
        raise ValueError("Hex strings must have the same length")

    diff = []
    for i in range(0, len(hex1), 2):
        byte1 = hex1[i:i+2]
        byte2 = hex2[i:i+2]
        if byte1 != byte2:
            diff.append((i//2, byte1, byte2))

    return diff


def xor_hex_strings(hex1, hex2):
    if len(hex1) != len(hex2):
        raise ValueError("Hex strings must have the same length")

    byte1 = bytes.fromhex(hex1)
    byte2 = bytes.fromhex(hex2)
    xor_result = bytes([b1 ^ b2 for b1, b2 in zip(byte1, byte2)])
    return xor_result.hex()


def xor_dicts(mid_state1, mid_state2):
    for key1, val1 in mid_state1.items():
        for key2, val2 in mid_state2.items():
            if key1 == key2:
                xor_result = xor_hex_strings(val1, val2)
                print(f"{key1} {xor_result}")
