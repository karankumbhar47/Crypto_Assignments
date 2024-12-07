from utils import *

def KeyGen(key_128bit):
    key_0 = stringToHexList(key_128bit[:16])
    key_1 = stringToHexList(key_128bit[16:32])
    WK = list(int(a,16)^int(b,16) for a,b in zip(key_0,key_1))  
    for i in range(0,16):
        WK[i]=hex(WK[i])
    return WK,key_0,key_1

def KeyAdd (state, key, iteration):
    if (iteration == -1):
        state = list(int(str(a),16)^int(str(b),16) for a, b in zip(key, state))
    else:
        # round key generation
        k = list(int(str(a),16) ^ int(b) for a, b in zip(beta[iteration], key))
        state = list(int(str(a),16) ^ int(b) for a, b in zip(state, k))

    for i in range(0, 16):
        state[i] = hex(state[i])
    return state

def SubCell(state):
    for i in range(16):
        state[i] = hex(Sb0[int(str(state[int(i)]),16)])
    return state

def ShuffleCell(state):
    newIndices=[0,10,5,15,14,4,11,1,9,3,12,6,7,13,2,8]
    tempState = state[:]
    for i in range(16):
        tempState[i]= state[newIndices[i]]
    return tempState


def MixColumn(state):
    cell = state[0:16]  
    for i in range(0,4):
        state[i*4]=hex(int(str(cell[i*4+1]),16) ^ int(str(cell[i*4+2]),16)^int(str(cell[i*4+3]),16))
        state[i*4+1]=hex(int(str(cell[i*4]),16) ^ int(str(cell[i*4+2]),16)^int(str(cell[i*4+3]),16))
        state[i*4+2]=hex(int(str(cell[i*4]),16) ^ int(str(cell[i*4+1]),16)^int(str(cell[i*4+3]),16))
        state[i*4+3]=hex(int(str(cell[i*4]),16) ^ int(str(cell[i*4+1]),16)^int(str(cell[i*4+2]),16))
    return state


def InvSubCell(state):
    for i in range(16):
        state[i] = hex(InvSb0[int(str(state[int(i)]),16)])
    return state

def InvShuffleCell(state):
    invNewIndices = [0, 7, 14, 9, 5, 2, 11, 12, 15, 8, 1, 6, 10, 13, 4, 3]
    tempState = state[:]
    for i in range(16):
        tempState[i] = state[invNewIndices[i]]
    return tempState

def InvMixColumn(state):
    cell = state[:]
    for i in range(0, 4):
        state[i * 4] = hex(int(str(cell[i * 4 + 1]), 16) ^ int(str(cell[i * 4 + 2]), 16) ^ int(str(cell[i * 4 + 3]), 16))
        state[i * 4 + 1] = hex(int(str(cell[i * 4]), 16) ^ int(str(cell[i * 4 + 2]), 16) ^ int(str(cell[i * 4 + 3]), 16))
        state[i * 4 + 2] = hex(int(str(cell[i * 4]), 16) ^ int(str(cell[i * 4 + 1]), 16) ^ int(str(cell[i * 4 + 3]), 16))
        state[i * 4 + 3] = hex(int(str(cell[i * 4]), 16) ^ int(str(cell[i * 4 + 1]), 16) ^ int(str(cell[i * 4 + 2]), 16))
    return state

def Midori64_Core(plainText, WK, K0, K1):
    S = KeyAdd(plainText, WK,-1)
    for i in range(15):
        S = SubCell(S)
        S = ShuffleCell(S)
        S = MixColumn(S)
        S = KeyAdd(S, stringToIntList(K0 if i%2==0 else K1), i)
    S = SubCell(S)
    Y = KeyAdd(S, WK,-1)
    hex_string = ''.join(hex_val[2:] for hex_val in Y)
    return hex_string

def Midori64_Core_Decrypt(cipherText, WK, K0, K1):
    cipherText = stringToHexList(cipherText)
    S = KeyAdd(cipherText, WK, -1)
    S = InvSubCell(S)

    for i in range(14, -1, -1):
        S = KeyAdd(S, stringToIntList(K0 if i % 2 == 0 else K1), i)
        S = InvMixColumn(S)
        S = InvShuffleCell(S)
        S = InvSubCell(S)

    plainText = KeyAdd(S, WK, -1)
    hex_string = ''.join(hex_val[2:] for hex_val in plainText)
    return hex_string
