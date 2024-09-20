from sypher004 import Sypher004
from utils import generate_message_pairs, generate_random_keys


def isOutDiff_2(output1, output2):
    diff = output1 ^ output2
    return diff == 32


def experiment():
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
