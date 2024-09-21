
sbox = [12,15,7,3,5,9,10,2,14,11,6,1,0,4,13,8]

ans = [[0 for i in range (16)]for j in range(16)]

for x in range(16):
    for dx in range(16):
        dy = sbox[x] ^ sbox[x ^ dx]
        ans[dx][dy] += 1

for i in ans:
    print(i)
	


    
