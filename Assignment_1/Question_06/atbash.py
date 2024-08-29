def decrypt(cipher):
        mssge = ""
        for i in cipher:
            if i.isalpha():
                if i.islower():
                    mssge += chr(122-ord(i)+97)
                else:
                    mssge += chr(90-ord(i)+65)
            else:
                mssge += i
        return mssge
    
print(decrypt("XZKVIXZROORV"))