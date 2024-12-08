# import numpy as np
# from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes

# # Midori S-box for SubBytes step

# MIDORI_SBOX = [0xC, 0xA, 0xD, 0x3, 0xE, 0xB, 0xF, 0x7, 0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6]


from array import *
import numpy as np
import copy
beta=[[0,0,0,1,0,1,0,1,1,0,1,1,0,0,1,1],[0,1,1,1,1,0,0,0,1,1,0,0,0,0,0,0],
                [1,0,1,0,0,1,0,0,0,0,1,1,0,1,0,1],[0,1,1,0,0,0,1,0,0,0,0,1,0,0,1,1],
                [0,0,0,1,0,0,0,0,0,1,0,0,1,1,1,1],[1,1,0,1,0,0,0,1,0,1,1,1,0,0,0,0],
                [0,0,0,0,0,0,1,0,0,1,1,0,0,1,1,0],[0,0,0,0,1,0,1,1,1,1,0,0,1,1,0,0],
                [1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,1],[0,1,0,0,0,0,0,0,1,0,1,1,1,0,0,0],
                [0,1,1,1,0,0,0,1,1,0,0,1,0,1,1,1],[0,0,1,0,0,0,1,0,1,0,0,0,1,1,1,0],
                [0,1,0,1,0,0,0,1,0,0,1,1,0,0,0,0],[1,1,1,1,1,0,0,0,1,1,0,0,1,0,1,0],
                [1,1,0,1,1,1,1,1,1,0,0,1,0,0,0,0]]                
 
def stringToHexList(string_input):
    hex_list = []
    for i in range(len(string_input)):
        hex_list.append(hex(int(str(string_input[i]),16)))
    return hex_list
 
def stringToIntList(string_input):
    int_list = []
    for i in range(len(string_input)):
        int_list.append(int(str(string_input[i]),16))
    return int_list

def KeyGen(key_128bit):
    K0 = stringToHexList(key_128bit[:16])
    K1 = stringToHexList(key_128bit[16:32])
    WK = list(int(a,16)^int(b,16) for a,b in zip(K0,K1))  
    for i in range(0,16):
        WK[i]=hex(WK[i])
    return WK,K0,K1

def KeyAdd (state, key, iteration):
    if (iteration == -1):
        state = list(int(str(a),16)^int(str(b),16) for a, b in zip(key, state))
        print("STATE",state)
        for i in range(0, 16):
            state[i] = hex(state[i])
    else:
        k = list(int(str(a),16) ^ int(b) for a, b in zip(beta[iteration], key))
        state = list(int(str(a),16) ^ int(b) for a, b in zip(state, k))
        for i in range(0, 16):
            state[i] = hex(state[i])
    return state

Sb0 = [0xc,0xa,0xd,0x3,0xe,0xb,0xf,0x7,0x8,0x9,0x1,0x5,0x0,0x2,0x4,0x6]
def SubCell(state):
    for i in range(16):
        state[i] = hex(Sb0[int(str(state[int(i)]),16)])
    return state

def ShuffleCell(state):
    newIndices=[0,10,5,15,14,4,11,1,9,3,12,6,7,13,2,8]
    tempState = copy.deepcopy(state)
    for i in range(16):
        tempState[i]= state[newIndices[i]]
    return tempState

def MixColumn(state):
    cell = copy.deepcopy(state)
    for i in range(0,4):
            state[i*4]=hex(int(str(cell[i*4+1]),16) ^ int(str(cell[i*4+2]),16)^int(str(cell[i*4+3]),16))
            state[i*4+1]=hex(int(str(cell[i*4]),16) ^ int(str(cell[i*4+2]),16)^int(str(cell[i*4+3]),16))
            state[i*4+2]=hex(int(str(cell[i*4]),16) ^ int(str(cell[i*4+1]),16)^int(str(cell[i*4+3]),16))
            state[i*4+3]=hex(int(str(cell[i*4]),16) ^ int(str(cell[i*4+1]),16)^int(str(cell[i*4+2]),16))
    return state


def isBalanced(elements):
    xor_result = 0  # Initialize XOR result as 0
    for elem in elements:
        # Get the first element of the sublist (index 0)
        sub_elem = elem
        # Remove '0x' prefix and convert to integer
        value = int(sub_elem, 16)
        xor_result ^= value  # Perform XOR
    return xor_result == 0  # Check if the result is 0 (balanced)
    # if not elements:
    #     return True  # Return True if the input is empty
    
    # num_columns = len(elements[0])  # Get the number of columns
    # xor_results = [0] * num_columns  # Initialize XOR results for all columns
    
    # for row in elements:
    #     for col_index in range(num_columns):
    #         # Convert each element in the column to an integer (assuming hex format)
    #         value = int(row[col_index], 16)
    #         xor_results[col_index] ^= value  # Perform XOR for the column
    # return xor_results

def isAll(arr):
    print(type(arr[0]))
    if all(int(i, 16) < 16 for i in arr):
        return len(arr) == 16 and len(np.unique(arr)) == len(arr) 

def isConstant(array):
    return np.all(array == array[0])

def Midori64_Core():
    # S = KeyAdd(plainText, WK,-1)
    # for i in range(4):
    #     S = SubCell(S)
    #     S = ShuffleCell(S)
    #     S = MixColumn(S)
    #     S = KeyAdd(S, stringToIntList(K0 if i%2==0 else K1), i)
    #     print(f"S round : {i}", S)
    # S = SubCell(S)
    # Y = KeyAdd(S, WK,-1)
    # return S
    key_128Bit = "687ded3b3c85b3f35b1009863e2a8cbf"
    WK, K0, K1 = KeyGen(key_128Bit)
    plaintexts = []
    l = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
    for i in range(16):
        # plaintexts.append(f"2{l[i]}{l[i]}{l[i]}34{l[i]}{l[i]}5{l[i]}6{l[i]}7{l[i]}{l[i]}8")
        plaintexts.append(f"{l[i]}329252243272412")
    # print("PLAINTEXTS",plaintexts)
    for k in range(16):
        S = KeyAdd(plaintexts[k], WK,-1)
        plaintexts[k] = S
    # print("PLAINTEXTS1",plaintexts)
    temp = copy.deepcopy(plaintexts)
    for k in range(16):
        for l in range(16):
            temp[k][l] = plaintexts[l][k]
    # print("TEMP",temp)
    # for k in range(16):
    #         if isAll(temp[k]):
    #             print("Yes it is all")
    #         if isConstant(temp[k]):
    #             print("Yes it is constant")
    #         if isBalanced(temp[k]):
    #             print(f"Yes it is balanced: {k}")
    for i in range(4):
        for j in range(16):
            S = SubCell(plaintexts[j])
            S = ShuffleCell(S)
            S = MixColumn(S)
            S = KeyAdd(S, stringToIntList(K0 if i%2==0 else K1), i)
            # print(f"S round : {i}-{j}", S)

            plaintexts[j] = S
        temp = copy.deepcopy(plaintexts)
        for k in range(16):
            for l in range(16):
                temp[k][l] = plaintexts[l][k]
        for k in range(16):
            if isAll(temp[k]):
                print(f"Yes it is all: {i}-{k}")
            if isBalanced(temp[k]):
                print(f"Yes it is balanced: {i}-{k}")
            
    
    
    # plainText = "42c20fd3b586879e"
    # expected_output = "66bcdc6270d901cd"
    # res = []
    # for i in range(16):
    #     print("Output from Algorithm: ", Midori64_Core(plaintexts[i], WK, K0, K1))
    #     res.append(Midori64_Core(plaintexts[i], WK, K0, K1))
    # print(res)
    # print("Yes it is balanced: ", isBalanced(res))




Midori64_Core()



# l = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]


# plaintexts = []
# for i in range(16):
#     # plaintexts.append(f"2{l[i]}{l[i]}{l[i]}34{l[i]}{l[i]}5{l[i]}6{l[i]}7{l[i]}{l[i]}8")
#     plaintexts.append(f"{l[i]}{l[i]}{l[i]}{l[i]}{l[i]}{l[i]}{l[i]}{l[i]}{l[i]}{l[i]}{l[i]}{l[i]}{l[i]}{l[i]}{l[i]}{l[i]}")

        

# key_128Bit = "687ded3b3c85b3f35b1009863e2a8cbf"
# WK, K0, K1 = KeyGen(key_128Bit)
# # plainText = "42c20fd3b586879e"
# expected_output = "66bcdc6270d901cd"
# res = []
# for i in range(16):
#     print("Output from Algorithm: ", Midori64_Core(plaintexts[i], WK, K0, K1))
#     res.append(Midori64_Core(plaintexts[i], WK, K0, K1))
# # print(res)
# print("Yes it is balanced: ", isBalanced(res))
