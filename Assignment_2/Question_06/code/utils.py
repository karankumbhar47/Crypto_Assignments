import numpy as np
import subprocess

P_Box = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

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



# Utilit functions to analyze the diff 
def get_all_candidates(currdiff, ddt):
    candidates = []
    diffParts = [(currdiff >> (4 * j)) & 15 for j in range(4)]  

    for j, diff in enumerate(diffParts):
        for i in range(16):
            if ddt[diff][i] >=6:  
                mask = ~(15 << (4 * j))  
                new_diff = currdiff & mask  
                new_diff |= (i << (4 * j))  
                candidates.append(new_diff)
    return candidates               


# Utilit functions to analyze the diff 
def getAllPath(round: int,curr_path:list[int], all_path:list[list[int]],ddt):
    if(round==4):
        parts = [(curr_path[-1]>> (4 * j)) & 15 for j in range(4)]  # Extract 4 parts
        zero_count = sum(1 for part in parts if part == 0)
        if zero_count == 2:
            all_path.append(curr_path.copy())
        return 

    all_diff = get_all_candidates(curr_path[-1],ddt);
    for diff in all_diff:
        permutaedDiff = apply_permutation(diff)

        parts = [(permutaedDiff>> (4 * j)) & 15 for j in range(4)]  # Extract 4 parts
        zero_count = sum(1 for part in parts if part == 0)
        if zero_count < 2:
            continue
        curr_path.append(permutaedDiff)

        getAllPath(round+1,curr_path,all_path,ddt)
        curr_path.pop()
    return
        

# Utility function to get all diff path given starting diff  
def generateDiffPath(input_diff : int):
    S_Box = [6, 4, 12, 5, 0, 7, 2, 14, 1, 15, 3, 13, 8, 10, 9, 11]
    ddt = generate_ddt(S_Box)
    allPath = []
    currPath = [input_diff]
    getAllPath(0,currPath, allPath, ddt) 

    unique_paths = set(tuple(path) for path in allPath)
    unique_paths_list = [list(path) for path in unique_paths]
    for path in unique_paths_list:
        active = 0
        for diff in path:
            hexNum = hex(diff)[2:].zfill(4)
            for i in hexNum:
                if(i!="0"): active+=1
            print(hexNum,end=" ")
        print(active)