# experiment_6_9.py

from utils import generate_message_pairs, generate_random_keys
from sypher004 import Sypher004


def filterMessage(output1, output2):
    """
    Checks if the difference has specific characteristics in its nibbles to determine 
    if the pair is valid.

    @param output1: First output value (ciphertext).
    @param output2: Second output value (ciphertext).
    @return: True if the pair meets the filtering criteria, False otherwise.
    """
    diff = output1 ^ output2
    parts = [(diff >> (4 * j)) & 15 for j in range(4)]

    if (parts[0] != 0 or parts[2] != 0 or parts[3] != 0):
        return False
    if (parts[1] in {1, 2, 9, 10}):
        return True

    return False


def experiment():
    """
    Generates message pairs, applies the encryption, and counts how often 
    the output pairs meet the filtering criteria.

    @return: A list of tuples containing:
             - key_list: Random keys used for encryption.
             - count: Number of valid output pairs based on the filter criteria.
             - probability: Probability of such pairs occurring.
    """
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
