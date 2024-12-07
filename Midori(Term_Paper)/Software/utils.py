beta = [
    [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1],
    [0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],
    [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0],
]

Sb0 = [0xC, 0xA, 0xD, 0x3, 0xE, 0xB, 0xF, 0x7, 0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6]
InvSb0 = [0]*16
for idx, i in enumerate(Sb0):
    InvSb0[i] = idx

def stringToHexList(string_input):
    hex_list = []
    for i in range(len(string_input)):
        hex_list.append(hex(int(str(string_input[i]), 16)))
    return hex_list


def stringToIntList(string_input):
    int_list = []
    for i in range(len(string_input)):
        int_list.append(int(str(string_input[i]), 16))
    return int_list

def messageToHexString(message):
    hex_string = ''.join(format(ord(char), '02x') for char in message)
    return hex_string

def hexToMessageString(hex_string):
    # Convert the hex string back to the original message
    message = bytes.fromhex(hex_string).decode('utf-8')
    return message
