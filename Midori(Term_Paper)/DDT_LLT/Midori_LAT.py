import numpy as np
from codeGenerator import generate_lat_table
from Midori_Utils import *


def calculate_lat(sbox):
    n = int(len(sbox).bit_length() - 1)  
    lat = np.zeros((1 << n, 1 << n), dtype=int)  

    for input_mask in range(1 << n):  
        for output_mask in range(1 << n):  
            count = 0
            for input_value in range(1 << n):  
                output_value = sbox[input_value]
                input_parity = bin(input_value & input_mask).count('1') % 2  
                output_parity = bin(output_value & output_mask).count('1') % 2  
                if input_parity == output_parity:
                    count += 1
            lat[input_mask, output_mask] = count - (1 << (n - 1))  

    return lat


def main():
    lat = calculate_lat(midori_sbox)
    print(seperator)
    print("\nLinear Approximation Table:\n")
    pretty_print_lat(lat)

    print(seperator)
    value_counts = count_values(lat)
    print_value_counts(value_counts)

    print(seperator)
    row_counts = count_row_values(lat)
    column_counts = count_column_values(lat)

    print_counts(row_counts, label="Row")
    print(seperator)
    print_counts(column_counts, label="Column")

    row_sums, col_sums = calculate_row_col_sums(lat)

    # Output the results
    print(seperator)
    print("Row-wise sums:", row_sums)
    print("Column-wise sums:", col_sums)

    print(seperator)
    is_symmetric_result = is_symmetric(lat)
    print("\nIs the LAT Matrix Symmetric?", is_symmetric_result)

    generate_lat_table(lat)


if __name__=="__main__":
    main()