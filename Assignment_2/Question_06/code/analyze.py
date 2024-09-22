# analyze.py

from utils import generate_ddt, apply_permutation, bit16_to_tuple, tuple_to_16bit

S_Box = [6, 4, 12, 5, 0, 7, 2, 14, 1, 15, 3, 13, 8, 10, 9, 11]
lookupTable = generate_ddt(sbox=S_Box)
threshold = 6


def is_valid_transition(x, y):
    return lookupTable[x][y] >= threshold


def calculate_transition_probability(node1, node2):
    pr_x_to_y = lookupTable[node1[0]][node2[0]]/16
    pr_x_to_w = lookupTable[node1[1]][node2[1]]/16
    pr_x_to_z = lookupTable[node1[2]][node2[2]]/16
    pr_x_to_k = lookupTable[node1[3]][node2[3]]/16
    pr = pr_x_to_y * pr_x_to_w * pr_x_to_z * pr_x_to_k
    return pr


def active_count(path):
    total = 0
    boolVar = False
    for i, node in enumerate(path):
        curr = sum(1 for val in node if val != 0)
        if (i == len(path)-1 and curr == 2):
            boolVar = True
        total += curr
    return [total, boolVar]


def dfs(current_node, depth, path, total_probability, paths):
    if depth == 4:
        if (active_count(path)[1]):
            paths.append((path[:], total_probability, active_count(path)[0]))
        return

    for next_node in generate_next_nodes(current_node):
        if is_valid_transition(current_node[0], next_node[0]) and \
           is_valid_transition(current_node[1], next_node[1]) and \
           is_valid_transition(current_node[2], next_node[2]) and \
           is_valid_transition(current_node[3], next_node[3]):

            transition_prob = calculate_transition_probability(
                current_node, next_node)
            new_total_probability = total_probability * transition_prob

            permuted_bits = apply_permutation(tuple_to_16bit(next_node))
            next_node = bit16_to_tuple(permuted_bits)
            path.append(next_node)
            dfs(next_node, depth + 1, path, new_total_probability, paths)
            path.pop()  # Backtrack


def generate_next_nodes(node):
    next_nodes = []
    for i in range(16):
        for j in range(16):
            for k in range(16):
                for l in range(16):
                    next_node = (i, j, k, l)
                    next_nodes.append(next_node)
    return next_nodes


def find_all_paths(source_node):
    paths = []
    dfs(source_node, 0, [source_node], 1, paths)
    return paths


def main():
    maxProb = 0
    maxPath = []
    box = 0
    for i in range(16):
        for j in range(16):
            for k in range(16):
                for l in range(16):
                    source_node = (i, j, k, l)
                    all_paths = find_all_paths(source_node)

                    # Print the paths and their probabilities
                    for path, probability, active_number in all_paths:
                        if (maxProb < probability):
                            maxProb = probability
                            maxPath = path
                            box = active_number
                        print(
                            f"Path: {path}, Probability: {probability}, Active Number: {active_number}")

    print("\nmost optimized path is ", maxPath)
    print("\nprob of maxPath ", maxProb)


main()

