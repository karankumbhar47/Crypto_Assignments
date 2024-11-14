import subprocess

SUBSTITUTION_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

INV_SUBSTITUTION_BOX = {v: k for k, v in SUBSTITUTION_BOX.items()}

ROUND_CONSTANTS = [0x1, 0x2, 0x4, 0x8, 0x3]

def gf_mult(x, y):
    product = 0
    for _ in range(4):
        if y & 1:
            product ^= x
        carry = x & 0x8
        x = (x << 1) & 0xF
        if carry:
            x ^= 0x3
        y >>= 1
    return product

def generate_round_keys(init_key):
    key_layout = [[init_key[0], init_key[2]], [init_key[1], init_key[3]]]
    all_keys = [key_layout]
    for idx in range(5):
        mid_val = SUBSTITUTION_BOX[key_layout[1][1]]
        mid_val ^= ROUND_CONSTANTS[idx]
        next_key_layout = [
            [mid_val ^ key_layout[0][0], mid_val ^ key_layout[0][0] ^ key_layout[1][0] ^ key_layout[0][1]],
            [mid_val ^ key_layout[0][0] ^ key_layout[1][0], mid_val ^ key_layout[0][0] ^ key_layout[1][0] ^ key_layout[0][1] ^ key_layout[1][1]]
        ]
        all_keys.append(next_key_layout)
        key_layout = next_key_layout
    return all_keys

def apply_round_key(data_state, r_key):
    return [data_state[i] ^ r_key[i] for i in range(4)]

def reverse_row_shift(data_state):
    return [data_state[0], data_state[3], data_state[2], data_state[1]]

def inverse_substitute(data_state):
    return [INV_SUBSTITUTION_BOX[nib] for nib in data_state]

def inv_mix_columns(data_state):
    transformed = [
        gf_mult(data_state[0], 0x3) ^ gf_mult(data_state[1], 0x2),
        gf_mult(data_state[0], 0x2) ^ gf_mult(data_state[1], 0x3),
        gf_mult(data_state[2], 0x3) ^ gf_mult(data_state[3], 0x2),
        gf_mult(data_state[2], 0x2) ^ gf_mult(data_state[3], 0x3)
    ]
    return transformed

def hex_to_nibbles(hex_val):
    hex_int = int(hex_val, 16)
    nibbles_array = []
    for j in range(4):
        nib = (hex_int >> (12 - 4 * j)) & 0xF
        nibbles_array.append(nib)
    return nibbles_array

def nibbles_to_hex_str(nib_array):
    hex_int = 0
    for j, nib in enumerate(nib_array):
        hex_int |= (nib << (12 - 4 * j))
    return hex(hex_int)[2:]

def oracle_encrypt(binary_path, data_input):
    hex_input = nibbles_to_hex_str(data_input)
    result = subprocess.run([binary_path], input=hex_input, capture_output=True, text=True)
    if result.returncode == 0:
        cipher_hex = result.stdout[-5:-1]
        return hex_to_nibbles(cipher_hex)

def reverse_key_schedule(final_rkey):
    current_key = [[final_rkey[0], final_rkey[2]], [final_rkey[1], final_rkey[3]]]
    for idx in range(5, 0, -1):
        temp_val = current_key[1][1] ^ current_key[0][1]
        xor_value = SUBSTITUTION_BOX[temp_val] ^ ROUND_CONSTANTS[idx - 1]
        current_key = [
            [xor_value ^ current_key[0][0], current_key[1][0] ^ current_key[0][1]],
            [current_key[1][0] ^ current_key[0][0], current_key[1][1] ^ current_key[0][1]]
        ]
    return [current_key[0][0], current_key[1][0], current_key[0][1], current_key[1][1]]
