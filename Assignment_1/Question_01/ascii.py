def chipherToAscii():
    char_list = []

    with open('cipherText.txt', 'r') as file:
        txt = file.readlines()
        isblack = True
        for line in txt:
            if (isblack):
                for c in line[:-1]:
                    if (ord(c) != 10):
                        char_list.append(ord(c))
            else:
                for i in range(0, len(line)-1, 2):
                    num = int(line[i:i+2], 16)
                    if (num != 10):
                        char_list.append(num)
            isblack = not (isblack)

    return char_list


def getPatternIndex(cipherText):
    guessIndex = []
    for i in range(len(cipherText) - 18):
        if ((cipherText[i + 1] == cipherText[i+2]) and
            (cipherText[i+6] == cipherText[i+7]) and
            (cipherText[i+15] == cipherText[i+16])):
            guessIndex.append(i)
    return guessIndex
