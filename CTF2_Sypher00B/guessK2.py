def getCounters(T1_list, T0_list,messages,ciphers):
    for key in range(32):
        sbox = [15,	0,	9,	1,	12,	3,	25,	22,	4,	29,	7,	27,	16,	21,	26,	14,	31,	24,	2,	5,	28,	30,	10,	6,	17,	20,	19,	11, 18,	23,	13,	8]
        newCipher = sbox.index(key^ ciphers)
        alpha_x = Utils.getXor(30,messages)
        beta_sx = Utils.getXor(21, newCipher)
        if (alpha_x ^ beta_sx) == 1:
            T1_list[key]+=1
        else:
            T0_list[key]+=1
    return T1_list, T0_list

oracle_path = "./oracle08" 
messages, ciphers = Utils.getPairs(oracle_path)
alpha, beta , LAT = Utils.getMaskPairs()
T1_list = [0 for _ in range(32)]  
T0_list = [0 for _ in range(32)]
for i in range(32):
    T1_list, T0_list = getCounters(T1_list, T0_list, messages[i],ciphers[i])
   
maxx = 0
key = -1
for i in range(32):
    if abs(T1_list[i] - T0_list[i]) >= maxx:
        maxx = abs(T1_list[i] - T0_list[i])
        key = i
print(T1_list, T0_list, key)