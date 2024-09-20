from utils import generate_message_pairs, generate_random_keys
from sypher004 import Sypher004


def filterMessage(output1, output2):
    diff = output1 ^ output2
    parts = [(diff >> (4 * j)) & 15 for j in range(4)]

    if (parts[0] != 0 or parts[2] != 0 or parts[3] != 0):
        return False
    if (parts[1] == 1 or parts[1] == 2 or parts[1] == 9 or parts[1] == 10):
        return True

    return False


def experiment():
    message_pairs = generate_message_pairs()
    results = []

    for _ in range(6):
        count = 0
        key_list = generate_random_keys()

        for message, message_prime in message_pairs:
            ciphertext = Sypher004(message, key_list)[-1]
            ciphertext_prime = Sypher004(message_prime, key_list)[-1]

            if filterMessage(ciphertext, ciphertext_prime):
                count += 1

        probability = count / (2**16)
        results.append((key_list, count, probability))

    return results
