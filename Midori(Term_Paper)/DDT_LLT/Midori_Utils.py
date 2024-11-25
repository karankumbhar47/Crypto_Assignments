import numpy as np

midori_sbox = [0xC, 0xA, 0xD, 0x3, 0xE, 0xB, 0xF, 0x7, 0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6]
seperator = "\n"+"="*80+"\n"

def print_table(table):
    for row in table:
        print(" ".join(map(str, row)))


def count_values(table):
    value_counts = {}
    for row in table:
        for value in row:
            if value in value_counts:
                value_counts[value] += 1
            else:
                value_counts[value] = 1
    return value_counts


def print_value_counts(value_counts):
    print("Value Counts in the table:")
    for value, count in sorted(value_counts.items()):
        print(f"Value: {value}, Count: {count}")


def count_row_values(table):
    row_counts = []
    for row in table:
        counts = {}
        for value in row:
            if value in counts:
                counts[value] += 1
            else:
                counts[value] = 1
        row_counts.append(counts)
    return row_counts


def count_column_values(table):
    n = len(table)
    column_counts = [{} for _ in range(n)]
    for col in range(n):
        for row in range(n):
            value = table[row][col]
            if value in column_counts[col]:
                column_counts[col][value] += 1
            else:
                column_counts[col][value] = 1
    return column_counts


def print_counts(counts, label="Row"):
    print(f"{label}-wise Counts:")
    for idx, count in enumerate(counts):
        print(f"{label} {idx}: {dict(sorted(count.items()))}")


def calculate_row_col_sums(table):
    row_sums = [sum(row) for row in table]  
    col_sums = [sum(col) for col in zip(*table)]  
    return row_sums, col_sums


def pretty_print_lat(lat):
    for row in lat:
        print(" ".join(f"{val:3}" for val in row))


def is_symmetric(matrix):
    return np.array_equal(matrix, matrix.T)