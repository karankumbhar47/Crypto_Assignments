def shift_cipher(cipher):
    l = []

    for i in range(26):
        s = ""
        for j in cipher:
            if j == " ":
                s += " "
            elif j.islower():
                s += chr((ord(j) - ord('a') + i) % 26 + ord('a'))
            elif j.isupper():
                s += chr((ord(j) - ord('A') + i) % 26 + ord('A'))
            else:
                s += j  # Keeps non-alphabetic characters unchanged
        l.append(s)

    return l

if __name__ == '__main__':
    cipher = input("Enter the cipher text: ")
    l = shift_cipher(cipher)
    for i, shifted in enumerate(l):
        print(f"Shift {i}: {shifted}")

