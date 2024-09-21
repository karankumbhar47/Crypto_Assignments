# experiment_6_8.py

from sypher004 import Sypher004
from utils import generate_message_pairs, generate_random_keys


def isOutDiff_2(output1, output2):
    """
    Checks if the XOR difference between two outputs is 32.

    @param output1: First output value.
    @param output2: Second output value.
    @return: True if XOR difference is 32, False otherwise.
    """
    diff = output1 ^ output2
    return diff == 32


def experiment():
    """
    Runs a differential cryptanalysis experiment 6.8 using Sypher004.

    @return: A list of tuples with:
             - key_list: The random keys used.
             - count: Number of pairs with the desired output difference.
             - probability: Probability of such pairs occurring.
    """
    message_pairs = generate_message_pairs()
    results = []

    for _ in range(6):
        key_list = generate_random_keys()

        count = 0
        for message, message_prime in message_pairs:
            fourRoundOut = Sypher004(message, key_list)[4]
            fourRoundOut_prime = Sypher004(message_prime, key_list)[4]

            if isOutDiff_2(fourRoundOut, fourRoundOut_prime):
                count += 1

        probability = count / (2**16)
        results.append((key_list, count, probability))

    return results
