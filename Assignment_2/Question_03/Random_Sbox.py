import random

#	All the hexadecimal numbers used in sbox
HEX = [0,1,2,3,4,5,6,7,8,9,0xa,0xb,0xc,0xd,0xe,0xf]

#	Assigning values to each hex number and creating sbox
sbox = []
for i in HEX.copy():
	j = random.choice(HEX)    #Choose a randm element
	sbox.append((i,j))        #Add in sbox
	HEX.remove(j)            # remove from HEX list we we assigned it to some number
	
#	Printing sbox
print("Sbox:")
for i in sbox:
    print(i)

    