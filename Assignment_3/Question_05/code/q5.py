import numpy as np
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# AES S-box for SubBytes step
SBOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
]

# AES round transformations
def sub_bytes(state):
    return np.array([[SBOX[byte] for byte in s] for s in state], dtype=np.uint8)

def shift_rows(full_state):
    res = []
    for state in full_state:
        state = state.reshape(4, 4)
        state[1] = np.roll(state[1], -1)
        state[2] = np.roll(state[2], -2)
        state[3] = np.roll(state[3], -3)
        res.append(state.flatten())
    return np.array(res, dtype=np.uint8)

# def gmul(a, b):
#     """
#     Perform Galois Field multiplication of two bytes a and b in GF(2^8).
#     """
#     p = 0  # Product initialized to 0
#     for i in range(8):  # Iterate over each bit
#         if b & 1:  # If the lowest bit of b is set, add a to the product
#             p ^= a
#         # Shift b to the right by 1 (divide by 2)
#         b >>= 1
#         # Shift a to the left by 1 (multiply by 2)
#         # If a overflows (>= 256), reduce modulo 0x11b
#         a = (a << 1) ^ 0x11b if a & 0x80 else a << 1
#     return p & 0xFF  # Return the result modulo 256

def gmul(a, b):
    p = 0
    for i in range(8):
        if (b >> i) & 1:
            p ^= a
        high_bit = a & 0x80
        a = (a << 1) & 0xFF  # Ensure 'a' stays within 8 bits
        if high_bit:
            a ^= 0x1b  # Apply the reduction polynomial (x^8 + x^4 + x^3 + x + 1)
    return p


def mix_columns(full_state):
    """
    Perform the AES MixColumns transformation in GF(2^8).
    Each column of the state is multiplied by the fixed matrix:
    [2 3 1 1]
    [1 2 3 1]
    [1 1 2 3]
    [3 1 1 2]
    """
    res = []
    for state in full_state:
        state = state.reshape(4, 4)  # Reshape to 4x4 matrix
        for col in range(4):
            # Extract the column
            a = state[:, col]
            # Perform Galois Field multiplications
            state[0, col] = gmul(a[0], 2) ^ gmul(a[1], 3) ^ gmul(a[2], 1) ^ gmul(a[3], 1)
            state[1, col] = gmul(a[0], 1) ^ gmul(a[1], 2) ^ gmul(a[2], 3) ^ gmul(a[3], 1)
            state[2, col] = gmul(a[0], 1) ^ gmul(a[1], 1) ^ gmul(a[2], 2) ^ gmul(a[3], 3)
            state[3, col] = gmul(a[0], 3) ^ gmul(a[1], 1) ^ gmul(a[2], 1) ^ gmul(a[3], 2)
        res.append(state.flatten())
    return np.array(res, dtype=np.uint8)



def add_round_key(state, key):
    for i in range(len(state)):
        for j in range(len(state[0])):
            state[i][j] ^= key[j]
    return np.array(state, dtype=np.uint8)

def aes_n_rounds(state, key, rounds):
    state = add_round_key(state, key)
    for _ in range(rounds):
        state = sub_bytes(state)
        state = shift_rows(state)
        if _ < rounds - 1:
            state = mix_columns(state)
        state = add_round_key(state, key)
    return state

# Distinguisher-related utilities
def isAll(arr):
    return len(arr) == 256 and len(np.unique(arr)) == len(arr)

def isConstant(array):
    return np.all(array == array[0])

def isBalanced(array):
    xor_result = 0
    for elem in array:
        xor_result ^= elem
    return xor_result == 0

def verify_3_round_integral_distinguisher():
    print("Verifying 3-round integral distinguisher on AES...")
    
    # Generate 256 plaintexts with a single varying byte
    plaintexts = np.array([
        [i,2,4,5,6,8,9,10,11,12,13,14,15,16,17,18]  # Fixed plaintext with varying first byte
        for i in range(256)
    ], dtype=np.uint8)
    print(f"Generated {len(plaintexts)} plaintexts with a single varying byte.", plaintexts)

    # Encrypt the plaintexts through 3 rounds of AES
    state = plaintexts.copy()
    state = add_round_key(state, get_random_bytes(16))
    for round_num in range(1, 4):
        print(f"Round {round_num}:")
        # Apply AES round transformations
        state = sub_bytes(state)  # Updated sub_bytes handles arrays
        state = shift_rows(state)
        # if round_num < 3:  # MixColumns is not applied in the last round
        state = mix_columns(state)
        # if round_num < 3:  # MixColumns is not applied in the last round
        state = add_round_key(state, get_random_bytes(16))

        # Analyze each column for the integral property
        # state = np.asarray(state, dtype=np.uint8)

        # Transpose the state array (interchange rows and columns)
        transposed_state = np.transpose(state)
        # state = state.reshape(-1, 4, 4)  # Reshape for column-wise operations
        count = 0
        for row in transposed_state:
            print(f" Round no: {round_num}")
            print(f"  Column no: {count}")
            print(f" Column: {row} ")
            print(f"    Is All (0-255)? {'Yes' if isAll(row) else 'No'}")
            print(f"    Is Constant? {'Yes' if isConstant(row) else 'No'}")
            print(f"    Is Balanced (sum = 0 mod 256)? {'Yes' if isBalanced(row) else 'No'}")
            count += 1

    print("\nVerification complete!")

# Run the verification
verify_3_round_integral_distinguisher()
