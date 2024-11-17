import Utils

## recurrsively eliminate the key space
def solver(T1_list, T0_list, alpha, beta):
    keys = [(i, j) for i in range(32) for j in range(32)]
    tested_keys_1 = set(keys)
    for idx in range(len(alpha)):
        for k0, k1 in keys:
            alpha_k0 = Utils.getXor(alpha[idx], k0)
            beta_k1 = Utils.getXor(beta[idx], k1)

            if T1_list[idx] > T0_list[idx]:
                if alpha_k0^beta_k1 != 1:
                    tested_keys_1.remove((k0, k1))
            elif T1_list[idx] < T0_list[idx]: 
                if alpha_k0^beta_k1 != 0:
                    tested_keys_1.remove((k0,k1))

        keys = list(tested_keys_1)
        print(idx ," keys :", keys)
        if len(keys) == 1:
            print("keys :", keys)
            return keys
        # if len(keys) == 0:
        #     break
    return 


## returing T0 and T1 counters
def getCounters(alpha,beta,messages,ciphers,LAT):
    T1_list = []
    T0_list = []
    for idx in range(len(alpha)):
        T1 = 0
        T0 = 0
        for i in range(32):
            alpha_x = Utils.getXor(alpha[idx],i)
            beta_sx = Utils.getXor(beta[idx], ciphers[i])
            if (alpha_x ^ beta_sx) == 1:
                T1+= 1
            else:
                T0+= 1
        if(LAT[alpha[idx]][beta[idx]] > 0):
            T1_list.append(T1)
            T0_list.append(T0)
        else:
            T0_list.append(T1)
            T1_list.append(T0)
    return T1_list, T0_list


def getk2(alpha,beta,messages,ciphers,LAT):
    for idx in range(len(alpha)):
        T1_list = [0 for _ in range(32)]
        T0_list = [0 for _ in range(32)]
        for i in range(32):
            alpha_x = Utils.getXor(alpha[idx],i)
            beta_sx = Utils.getXor(beta[idx], reduce_round(ciphers[i], i))
            if (alpha_x ^ beta_sx) == 1:
                T1_list[i] += 1
            else:
                T0_list[i] += 1
        # if(LAT[alpha[idx]][beta[idx]] > 0):
        #     T1_list.append(T1)
        #     T0_list.append(T0)
        # else:
        #     T0_list.append(T1)
        #     T1_list.append(T0)
    print(T1_list)
    print(T0_list)
    maxx = 0
    key_candidates = []
    for i in range(32):
        if maxx < abs(T1_list[i]- T0_list[i]):
            maxx = abs(T1_list[i]- T0_list[i])
            key_candidates = []
            key_candidates.append(i)
        elif maxx == abs(T1_list[i]- T0_list[i]):
            key_candidates.append(i)

    return key_candidates


sbox = [15, 0, 9, 1, 12, 3, 25, 22, 4, 29, 7, 27, 16, 21, 26, 14,31, 24, 2, 5, 28, 30, 10, 6, 17, 20, 19, 11, 18, 23, 13, 8]
def reduce_round(c,k2):
    xor = c^k2
    return sbox.index(xor)



def main():
    oracle_path = "./oracle08" 
    messages, ciphers = Utils.getPairs(oracle_path)
    alpha, beta , LAT = Utils.getMaskPairs()
    k2_cand = [17]
    for k2 in k2_cand:
        cipher_list = [reduce_round(c,k2) for c in ciphers]
        T1,T0 = getCounters(alpha,beta,messages,cipher_list,LAT)
        solver(T1, T0, alpha, beta)
    # k2_max = 0
    # for k2 in range(32):
    #     k2_max= max(k2_max,abs(T1_list[k2] - T0_list[k2]))

    
if __name__=="__main__":
    main()
