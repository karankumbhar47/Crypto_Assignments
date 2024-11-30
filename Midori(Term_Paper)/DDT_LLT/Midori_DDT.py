import numpy as np
from codeGenerator import *
from Midori_Utils import *

def generate_ddt(sbox):
    n = len(sbox)  
    ddt = [[0] * n for _ in range(n)]  

    for x1 in range(n):
        for x2 in range(n):
            delta_in = x1 ^ x2  
            delta_out = sbox[x1] ^ sbox[x2]  
            ddt[delta_in][delta_out] += 1  

    return ddt

def main():
    ddt = generate_ddt(midori_sbox)
    print(ddt)
    print(seperator)
    print("\nDifferential Distribution Table (DDT):\n")
    print_table(ddt)

    print(seperator)
    value_counts = count_values(ddt)
    print_value_counts(value_counts)

    print(seperator)
    row_counts = count_row_values(ddt)
    column_counts = count_column_values(ddt)

    print_counts(row_counts, label="Row")
    print(seperator)
    print_counts(column_counts, label="Column")

    row_sums, col_sums = calculate_row_col_sums(ddt)

    # Output the results
    print(seperator)
    print("Row-wise sums:", row_sums)
    print("Column-wise sums:", col_sums)

    print(seperator)
    is_symmetric_result = is_symmetric(np.array(ddt))
    print("\nIs the DDT Matrix Symmetric?", is_symmetric_result)

    generate_ddt_latex(ddt)
    generate_sbox_latex(midori_sbox)


if __name__=="__main__":
    main()