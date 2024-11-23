beta=[[0,0,0,1,0,1,0,1,1,0,1,1,0,0,1,1],[0,1,1,1,1,0,0,0,1,1,0,0,0,0,0,0],
                [1,0,1,0,0,1,0,0,0,0,1,1,0,1,0,1],[0,1,1,0,0,0,1,0,0,0,0,1,0,0,1,1],
                [0,0,0,1,0,0,0,0,0,1,0,0,1,1,1,1],[1,1,0,1,0,0,0,1,0,1,1,1,0,0,0,0],
                [0,0,0,0,0,0,1,0,0,1,1,0,0,1,1,0],[0,0,0,0,1,0,1,1,1,1,0,0,1,1,0,0],
                [1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,1],[0,1,0,0,0,0,0,0,1,0,1,1,1,0,0,0],
                [0,1,1,1,0,0,0,1,1,0,0,1,0,1,1,1],[0,0,1,0,0,0,1,0,1,0,0,0,1,1,1,0],
                [0,1,0,1,0,0,0,1,0,0,1,1,0,0,0,0],[1,1,1,1,1,0,0,0,1,1,0,0,1,0,1,0],
                [1,1,0,1,1,1,1,1,1,0,0,1,0,0,0,0]]                
 
Sb0 = [0xc,0xa,0xd,0x3,0xe,0xb,0xf,0x7,0x8,0x9,0x1,0x5,0x0,0x2,0x4,0x6]

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