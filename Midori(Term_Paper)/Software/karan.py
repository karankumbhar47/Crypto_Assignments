from Midori import *

class ECBMode:
    BLOCK_SIZE = 8 # Example block size in bytes

    def __init__(self, encrypt_block, decrypt_block):
        key_128Bit = "687ded3b3c85b3f35b1009863e2a8cbf"
        self.WK, self.K0, self.K1 = KeyGen(key_128Bit)
        self.encrypt_block = encrypt_block
        self.decrypt_block = decrypt_block

    def pad(self, data):
        pad_length = self.BLOCK_SIZE - len(data) % self.BLOCK_SIZE
        return data + bytes([pad_length] * pad_length)

    def unpad(self, data):
        pad_length = data[-1]
        return data[:-pad_length]

    def encrypt_ecb(self, plaintext):
        plaintext = self.pad(plaintext)
        num_blocks = len(plaintext) // self.BLOCK_SIZE
        ciphertext = ''

        for i in range(num_blocks):
            block = plaintext[i * self.BLOCK_SIZE:(i + 1) * self.BLOCK_SIZE]
            ciphertext += self.encrypt_block(block.hex(), self.WK, self.K0, self.K1)

        return ciphertext

    def decrypt_ecb(self, ciphertext):
        ciphertext = bytes.fromhex(ciphertext)
        num_blocks = len(ciphertext) // self.BLOCK_SIZE
        plaintext = ''

        for i in range(num_blocks):
            block = ciphertext[i * self.BLOCK_SIZE:(i + 1) * self.BLOCK_SIZE]
            plaintext += self.decrypt_block(block.hex(), self.WK, self.K0, self.K1)

        return self.unpad(bytes.fromhex(plaintext)).decode('utf-8')


ecb = ECBMode(Midori64_Core, Midori64_Core_Decrypt)

out = ecb.encrypt_ecb(b'karansunilkumbhar')
out = ecb.decrypt_ecb(out)
print(out)