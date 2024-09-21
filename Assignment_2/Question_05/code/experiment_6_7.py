# experiment_6_7.py
from sypher004 import Sypher004
from utils import generate_message_pairs, generate_random_keys


def isOutDiff_2(allRoundOut1, allRoundOut2):
    """
    Checks if the XOR difference between two sets of round outputs is 32.

    @param allRoundOut1: List of output values for the first message.
    @param allRoundOut2: List of output values for the second message.
    @return: True if the XOR difference between corresponding outputs equals 32, otherwise False.
    """
    for i in range(len(allRoundOut1)):
        output1 = allRoundOut1[i]
        output2 = allRoundOut2[i]
        diff = output1 ^ output2
        if (diff != 32):
            return False
    return True


def experiment():
    """
    Runs a differential cryptanalysis experiment 6.7 using Sypher004.

    @return: A list of tuples with:
             - key_list: The random keys used.
             - count: The number of pairs with the desired output difference.
             - probability: Probability of such pairs occurring.
    """
    message_pairs = generate_message_pairs()
    results = []

    for _ in range(6):
        key_list = generate_random_keys()

        count = 0
        for message, message_prime in message_pairs:
            allRoundOutC = Sypher004(message, key_list)
            allRoundOutC_prime = Sypher004(message_prime, key_list)

            if isOutDiff_2(allRoundOutC[:-1], allRoundOutC_prime[:-1]):
                count += 1

        probability = count / (2**16)
        results.append((key_list, count, probability))

    return results
