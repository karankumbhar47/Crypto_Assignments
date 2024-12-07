from Midori import *

class ECBMode:
    def __init__(self, encrypt_block, decrypt_block, key):
        self.key_128Bit = key 
        self.WK, self.K0, self.K1 = KeyGen(self.key_128Bit)
        self.encrypt_block = encrypt_block
        self.decrypt_block = decrypt_block
        self.BLOCK_SIZE = 16 

    def pad(self, data):
        byteData = bytes.fromhex(data)
        pad_length = self.BLOCK_SIZE - len(byteData) % self.BLOCK_SIZE
        return (byteData + bytes([pad_length] * pad_length)).hex()

    def unpad(self, data):
        byteData = bytes.fromhex(data)
        pad_length = byteData[-1]
        return byteData[:-pad_length].hex()

    def encrypt_ecb(self, plaintext):
        plaintext = ''.join(format(ord(char), '02x') for char in plaintext)
        plaintext = self.pad(plaintext)
        num_blocks = len(plaintext) // self.BLOCK_SIZE
        ciphertext = ''

        for i in range(num_blocks):
            block = plaintext[i * self.BLOCK_SIZE:(i + 1) * self.BLOCK_SIZE]
            ciphertext += self.encrypt_block(block, self.WK, self.K0, self.K1)

        return ciphertext

    def decrypt_ecb(self, ciphertext):
        num_blocks = len(ciphertext) // self.BLOCK_SIZE
        plaintext = ''

        for i in range(num_blocks):
            block = ciphertext[i * self.BLOCK_SIZE:(i + 1) * self.BLOCK_SIZE]
            plaintext += self.decrypt_block(block, self.WK, self.K0, self.K1)

        plaintext = self.unpad(plaintext)
        message = bytes.fromhex(plaintext).decode('utf-8')
        return message


ecb = ECBMode(Midori64_Core, Midori64_Core_Decrypt,"687ded3b3c85b3f35b1009863e2a8cbf")

message = "message random message "
out = ecb.decrypt_ecb(ecb.encrypt_ecb(message))
print(out==message)