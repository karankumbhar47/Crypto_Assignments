def modinv(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def encrypt(mssge,a,b):
    c = ""
    for i in mssge:
        if i.isalpha():
            if i.islower():
                c += chr(((a*(ord(i)-97)+b)%26)+97)
            else:
                c += chr(((a*(ord(i)-65)+b)%26)+65)
        else:
            c += i
    return c

def decrypt(cipher, a, b):
    mssge = ""
    for i in cipher:
        if i.isalpha():
            if i.islower():
                mssge += chr(((modinv(a, 26)*(ord(i)-97-b))%26)+97)
            else:
                mssge += chr(((modinv(a, 26)*(ord(i)-65-b))%26)+65)
        else:
            mssge += i
    return mssge

cipher = encrypt("cryptography", 3, 5)
print("ciphertext of encrypted 'cryptography' : ", cipher)
print("decryption of 'XRHLAFUUK' : ", decrypt("XRHLAFUUK", 3, 5))
