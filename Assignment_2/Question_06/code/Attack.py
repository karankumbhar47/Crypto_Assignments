import random
from utils import *
from sypher004 import Sypher004

SBox = [0x6, 0x4, 0xC, 0x5, 0x0, 0x7, 0x2, 0xE,
        0x1, 0xF, 0x3, 0xD, 0x8, 0xA, 0x9, 0xB]
InverseSBox = [SBox.index(i) for i in range(16)]

DDT = generate_ddt(SBox) 


def reverse_last_round(ciphertext, round_key):
    return InverseSBox[ciphertext ^ round_key]


def differential_attack(plaintext_pairs, round_keys):
    guessed_keys = {}
    for k5_guess in range(16):  
        matches = 0
        for pt1, pt2 in plaintext_pairs:
            ct1 = Sypher004(pt1, round_keys)[-1]  
            ct2 = Sypher004(pt2, round_keys)[-1]  
            r4_output1 = reverse_last_round(ct1, k5_guess)
            r4_output2 = reverse_last_round(ct2, k5_guess)
            if r4_output1 ^ r4_output2 == expected_difference:
                matches += 1
        guessed_keys[k5_guess] = matches
    return max(guessed_keys, key=guessed_keys.get)

plaintext_pairs = generate_message_pairs(0,0,0,f)
round_keys = [random.randint(0, 15) for _ in range(5)] 
expected_difference = 0x6  


best_key_guess = differential_attack(plaintext_pairs, round_keys)
print(f"Best key guess for K5: {best_key_guess}")

"""
x06 = 1
x17 = 1
x2c = 1 
x30 = 1
x31 = 1
x41 = 1
x46 = 1
"""
# 