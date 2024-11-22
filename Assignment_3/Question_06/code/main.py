from mode import *


def test_CBCMode(message, keys, iv):
    encrypted_cbc = encrypt_cbc(message, keys, iv)
    decrypted_cbc_bytes = decrypt_cbc(encrypted_cbc, keys, iv)

    print("---- CBC Mode ----\n")
    print("Encrypted (CBC):", encrypted_cbc)
    print("Decrypted (CBC):", decrypted_cbc_bytes.decode('utf-8', errors='ignore'))

    return encrypted_cbc


def error_cbc(encrypted_cbc, keys, iv):
    modified_cbc = flip_bit(encrypted_cbc, 1, 5)
    decrypted_cbc_error_bytes = decrypt_cbc(modified_cbc, keys, iv)

    print("Modified Ciphertext (CBC):", modified_cbc)
    print("Decrypted with Error (CBC):",
          decrypted_cbc_error_bytes.decode('utf-8', errors='ignore'))


def test_CFBMode(message, keys, iv):
    encrypted_cfb = encrypt_cfb(message, keys, iv)
    decrypted_cfb_bytes = decrypt_cfb(encrypted_cfb, keys, iv)

    print("---- CFB Mode ----\n")
    print("Encrypted (CFB):", encrypted_cfb)
    print("Decrypted (CFB):", decrypted_cfb_bytes.decode('utf-8', errors='ignore'))

    return encrypted_cfb

def error_cfb(encrypted_cfb, keys, iv):
    modified_cfb = flip_bit(encrypted_cfb, 1, 5)
    decrypted_cfb_error_bytes = decrypt_cfb(modified_cfb, keys, iv)

    print("Modified Ciphertext (CFB):", modified_cfb)
    print("Decrypted with Error (CFB):",
          decrypted_cfb_error_bytes.decode('utf-8', errors='ignore'))



def main():
    seperator = "\n"+"="*50+"\n"

    keys = [0x1234, 0x5678, 0x9ABC, 0xDEF0, 0x1357, 0x2468]
    iv = 0xA5A5
    message = "This".encode('utf-8')

    print(seperator)
    print("Message : ",message)
    print("IV      : ",iv)
    print("Keys    : ",keys)
    print(seperator)

    encrypted_cbc = test_CBCMode(message,keys,iv)
    print("\n")
    error_cbc(encrypted_cbc,keys,iv)
    print(seperator)

    encrypted_cfb = test_CFBMode(message,keys,iv)
    print("\n")
    error_cfb(encrypted_cfb,keys,iv)
    print(seperator)


if __name__ == "__main__":
    main()
