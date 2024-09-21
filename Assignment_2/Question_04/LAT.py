import numpy as np

sbox = [12, 15, 7, 3, 5, 9, 10, 2, 14, 11, 6, 1, 0, 4, 13, 8]

n = 4
size = 2**n

lat = np.zeros((size, size), dtype=int)

for a in range(size): 
    for b in range(size):
        count = 0

        for x in range(size):
            
            input_mask = bin(a & x).count('1') % 2

            output_mask = bin(b & sbox[x]).count('1') % 2

            if input_mask == output_mask:
                count += 1

        lat[a, b] = count - (size // 2)

print("Linear Approximation Table (LAT):")
print(lat)
