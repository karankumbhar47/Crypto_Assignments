# utils.py

import subprocess
from tabulate import tabulate


def generate_message_pairs():
    """
    generate 2^16 message pair with difference (0,0,2,0)

    @return: A list of tuples containing pairs of messages.
             Each tuple consists of (message, message_prime).
    """
    message_pairs = []

    for m in range(2**16):
        M0 = (m >> 12) & 15
        M1 = (m >> 8) & 15
        M2 = (m >> 4) & 15
        M3 = m & 15
        M2_prime = M2 ^ 0x2

        message = (M0 << 12) | (M1 << 8) | (M2 << 4) | M3
        message_prime = (M0 << 12) | (M1 << 8) | (M2_prime << 4) | M3
        message_pairs.append((message, message_prime))

    return message_pairs


def generate_random_keys() -> list[int]:
    """
    Generates a list of random keys using OpenSSL.

    @return: A list of integers representing the generated keys.
    """
    keys = []
    for _ in range(6):
        result = subprocess.run(['openssl', 'rand', '2'], capture_output=True)
        key = result.stdout.hex()
        keys.append(int(key, 16))
    return keys


def printResult(data: list[tuple]) -> None:
    table_data = []
    sum = 0
    for keys, count, prob in data:
        sum += count
        table_data.append([", ".join(map(str, keys)), count, prob])

    sum = sum/len(data)
    table_data.append(["Average", sum, sum/(2**16)])
    print(tabulate(table_data, headers=["Keys", "Count", "Probability"],
          tablefmt="grid", stralign="center", numalign="center", showindex=True))


def printLabel(label: str) -> None:
    print(f'\n {"="*74}\n')
    print(f'\n{" "*28} {label} \n')
