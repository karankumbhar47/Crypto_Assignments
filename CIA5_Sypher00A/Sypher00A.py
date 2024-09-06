import Utils

## recurrsively eliminate the key space
def solver(T1_list, T0_list, alpha, beta):
    keys = [(i, j) for i in range(16) for j in range(16)]
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
        if len(keys) == 1:
            print("keys :", keys)
            return keys
    return 


## returing T0 and T1 counters
def getCounters(alpha,beta,messages,ciphers,LAT):
    T1_list = []  
    T0_list = []
    for idx in range(len(alpha)):
        T1 = 0
        T0 = 0
        for i in range(16):
            alpha_x = Utils.getXor(alpha[idx],i)
            beta_sx = Utils.getXor(beta[idx], ciphers[i])
            if (alpha_x ^ beta_sx) == 1:
                T1+=1
            else:
                T0+=1
        if(LAT[alpha[idx]][beta[idx]] > 0):
            T1_list.append(T1)
            T0_list.append(T0)
        else:
            T0_list.append(T1)
            T1_list.append(T0)


def main():
    oracle_path = "./00Asypher_8" 
    messages, ciphers = Utils.getPairs(oracle_path)
    alpha, beta , LAT = Utils.getMaskPairs()
    T1,T0 = getCounters(alpha,beta,messages,ciphers,LAT)
    solver(T1, T0, alpha, beta)



if __name__=="__main__":
    main()