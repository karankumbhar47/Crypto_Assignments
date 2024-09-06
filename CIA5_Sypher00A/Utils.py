import subprocess

sbox = [15, 14, 11, 12, 6, 13, 7, 8, 0, 3, 9, 10, 4, 2, 1, 5]

# return the message and cipher text pair
# by multiple query to oracle
def getPairs(executable):
    message = []
    cipherText = []
    for i in range(16):
        result = subprocess.run([executable], input=str(i),
                                text=True, capture_output=True)
        lines = result.stdout.strip().split('\n')
        if len(lines) == 2:
            message_line = lines[0].strip()
            ciphertext_line = lines[1].strip()

            try:
                msg = int(message_line.split()[-1])
                cipher = int(ciphertext_line.split()[-1])
                message.append(msg)
                cipherText.append(cipher)
            except ValueError:
                print(
                    f"Failed to parse numbers from lines: {message_line}, {ciphertext_line}")

    return message, cipherText



# bitwise and of two numbers 
# And then xor of all bits of resultant number
def getXor(num1, num2):
    num = num1 & num2
    result = 0
    while num > 0:
        result ^= (num & 1)
        num >>= 1
    return result


# Creating LAT 
def createLat():
    ans = [[0 for _ in range(16)]for _ in range(16)]
    for x in range(1, 16):
        for y in range(1, 16):
            count = 0
            for z in range(16):
                alpha_x = getXor(x, z)
                beta_x = getXor(y, sbox[z])
                if alpha_x == beta_x:
                    count += 1
            ans[x][y] = count - 8
    return ans 


# Getting Alpha and Beta Mask value
# For getting eqution
def getMaskPairs():
    LAT = createLat()
    alpha = []
    beta = []
    for i in range(1, 16):
        for j in range(1, 16):
            if LAT[i][j] != 0 and abs(LAT[i][j]) != 2:
                alpha.append(i)
                beta.append(j)

    return alpha, beta, LAT 
