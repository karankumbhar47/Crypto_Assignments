#Randomly generated sbox

sbox = [12,15,7,3,5,9,10,2,14,11,6,1,0,4,13,8]

#	Creating matrix whose values are 0
ans = [[0 for i in range (16)]for j in range(16)]

# Calculate the DDT by finding input and output differences
for x in range(16):
    for dx in range(16):
        # Compute the output difference for S-box values
        dy = sbox[x] ^ sbox[x ^ dx]
        # Increment the count in the DDT table for this input-output difference pair (dx, dy)
        ans[dx][dy] += 1

#Printing the matrix
for i in ans:
    print(i)
	


    
