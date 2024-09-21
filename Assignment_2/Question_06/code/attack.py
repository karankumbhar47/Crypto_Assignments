from utils import *
from sypher004 import Sypher004

sbox = [0x6, 0x4, 0xc, 0x5, 0x0, 0x7, 0x2, 0xe,
        0x1, 0xf, 0x3, 0xd, 0x8, 0xa, 0x9, 0xb]
inversesbox = [sbox.index(i) for i in range(16)]

ddt = generate_ddt(sbox)


def match_bits(target: int, number: int) -> bool:
    extracted_bits = (number >> 4) & 0xff
    return extracted_bits == target


def isdiffmatches(output1, output2, diff):
    totaldiff = output1 ^ output2
    total_diff_parts = [(totaldiff >> (4 * j)) & 15 for j in range(4)]
    diff_parts = [(diff >> (4 * j)) & 15 for j in range(4)]
    if (diff_parts == total_diff_parts):
        return True
    return False


def reversedoutput(ciphertext, key):
    output_parts = [((ciphertext ^ key) >> (4 * j)) & 15 for j in range(4)]
    sbox_input_parts = [inversesbox[part] for part in output_parts]

    sbox_output = 0
    for j in range(4):
        sbox_output |= (sbox_input_parts[j] << (4 * j))
    return sbox_output


def differential_attack(plaintext_pairs, round_keys, expected_difference):
    guessed_keys = {}
    max_count = 0
    for k5_guess in range(256):
        matches = 0
        for pt1, pt2 in plaintext_pairs:
            ct1 = Sypher004(pt1, round_keys)[-1]
            ct2 = Sypher004(pt2, round_keys)[-1]

            r4_output1 = reversedoutput(ct1, k5_guess << 4)
            r4_output2 = reversedoutput(ct2, k5_guess << 4)

            if isdiffmatches(r4_output1, r4_output2, expected_difference):
                matches += 1
        guessed_keys[k5_guess] = matches
        print(k5_guess, guessed_keys[k5_guess])

        # update max_count
        if matches > max_count:
            max_count = matches

    # collect all keys with the maximum count
    best_keys = [key for key, count in guessed_keys.items()
                 if count == max_count]

    # verify each best key guess
    print("max count keys")
    print(best_keys)

    correct_keys = []
    for best_key in best_keys:
        if match_bits(best_key,round_keys[-1]):
            correct_keys.append(best_key)

    # return max(guessed_keys, key=guessed_keys.get)
    return best_keys, correct_keys


plaintext_pairs = generate_message_pairs(0, 2, 2, 0)
round_keys = generate_random_keys()
expected_difference = 0x220

best_key_guess, correct_keys = differential_attack(
    plaintext_pairs, round_keys, expected_difference)

print(round_keys)
print(f"best key guess for k5: {best_key_guess}")

if correct_keys:
    print("correct key guesses:", correct_keys)
else:
    print("no correct key guesses")
