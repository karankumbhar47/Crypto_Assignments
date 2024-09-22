# utils.py

import numpy as np
from sypher004 import Sypher004
import subprocess

P_Box = [0, 4, 8, 12,    1, 5, 9, 13,      2, 6, 10, 14,      3, 7, 11, 15]

def apply_permutation(input_bits : int) -> int:
    permuted_bits = 0
    for i in range(16):
        bit = (input_bits >> i) & 1
        permuted_bits |= (bit << P_Box[i])
    return permuted_bits

def generate_ddt(sbox):
    n = len(sbox)
    ddt = np.zeros((n, n), dtype=int)

    for d_in in range(n):
        for x in range(n):
            y1 = sbox[x]
            y2 = sbox[x ^ d_in]
            d_out = y1 ^ y2
            ddt[d_in][d_out] += 1
    return ddt


def generate_message_pairs(diff_0=0, diff_1=0, diff_2=0, diff_3=0):
    message_pairs = []

    for m in range(2**16):
        M0 = (m >> 12) & 15
        M1 = (m >> 8) & 15
        M2 = (m >> 4) & 15
        M3 = m & 15

        M0_prime = M0 ^ diff_0
        M1_prime = M1 ^ diff_1
        M2_prime = M2 ^ diff_2
        M3_prime = M3 ^ diff_3

        message = (M0 << 12) | (M1 << 8) | (M2 << 4) | M3
        message_prime = (M0_prime << 12) | (
            M1_prime << 8) | (M2_prime << 4) | M3_prime

        message_pairs.append((message, message_prime))
    return message_pairs


def generate_random_keys() -> list[int]:
    keys = []
    for _ in range(6):
        result = subprocess.run(['openssl', 'rand', '2'], capture_output=True)
        key = result.stdout.hex()
        keys.append(int(key, 16))
    return keys


def tuple_to_16bit(t: tuple) -> int:
    return (t[0] << 12) | (t[1] << 8) | (t[2] << 4) | t[3]

def bit16_to_tuple(n: int) -> tuple:
    x = (n >> 12) & 0xF  
    y = (n >> 8) & 0xF   
    z = (n >> 4) & 0xF   
    w = n & 0xF          
    return (x, y, z, w)


def filter_message(plainTextPair,keys):
    outputPlainText = []
    outputCipherText = []
    for p1, p2 in plainTextPair:
        c1 = Sypher004(p1,keys)[-1];
        c2 = Sypher004(p2,keys)[-1];
        if((c1^c2)>>8)==0:
            outputPlainText.append((p1,p2))
            outputCipherText.append((c1,c2))
    return outputPlainText,outputCipherText