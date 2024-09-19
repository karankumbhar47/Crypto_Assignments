import numpy as np

# Define the S-box
sbox = [12, 15, 7, 3, 5, 9, 10, 2, 14, 11, 6, 1, 0, 4, 13, 8]

# Define the size of the S-box (4-bit means 16 entries)
n = 4
size = 2**n

# Initialize the LAT (Linear Approximation Table)
lat = np.zeros((size, size), dtype=int)

# Compute the LAT
for a in range(size):  # Iterate over all input masks
    for b in range(size):  # Iterate over all output masks
        count = 0

        for x in range(size):  # Iterate over all possible inputs
            
            # Dot product (XOR) between input mask 'a' and input 'x'
            input_mask = bin(a & x).count('1') % 2

            # Dot product (XOR) between output mask 'b' and S-box output 'sbox[x]'
            output_mask = bin(b & sbox[x]).count('1') % 2

            # Check if input_mask == output_mask
            if input_mask == output_mask:
                count += 1
        # Populate the LAT with the biased result

        lat[a, b] = count - (size // 2)

# Print the LAT table
print("Linear Approximation Table (LAT):")
print(lat)
