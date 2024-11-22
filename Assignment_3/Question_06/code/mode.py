from utils import *
from sypher004 import *

# CBC Mode
def encrypt_cbc(plaintext: bytes, keys: list[int], iv: int) -> list[int]:
    blocks = split_into_blocks(plaintext)
    ciphertext = []
    previous_block = iv
    for block in blocks:
        xor_result = xor(block, previous_block)
        encrypted_block = sypher004_encrypt(xor_result, keys)
        ciphertext.append(encrypted_block)
        previous_block = encrypted_block
    return ciphertext


def decrypt_cbc(ciphertext: list[int], keys: list[int], iv: int) -> bytes:
    plaintext_blocks = []
    previous_block = iv
    for block in ciphertext:
        decrypted_block = xor(sypher004_decrypt(block, keys), previous_block)
        plaintext_blocks.append(decrypted_block)
        previous_block = block
    return combine_blocks(plaintext_blocks)


# CFB Mode
def encrypt_cfb(plaintext: bytes, keys: list[int], iv: int, t=4) -> list[int]:
    blocks = split_into_blocks(plaintext)
    ciphertext = []
    shift_register = iv
    for block in blocks:
        encrypted_register = sypher004_encrypt(shift_register, keys)
        ciphertext_block = xor(block, encrypted_register >> (16 - t))
        ciphertext.append(ciphertext_block)
        shift_register = ((shift_register << t) | ciphertext_block) & 0xFFFF
    return ciphertext


def decrypt_cfb(ciphertext: list[int], keys: list[int], iv: int, t=4) -> bytes:
    plaintext = []
    shift_register = iv
    for block in ciphertext:
        encrypted_register = sypher004_encrypt(shift_register, keys)
        plaintext_block = xor(block, encrypted_register >> (16 - t))
        plaintext.append(plaintext_block)
        shift_register = ((shift_register << t) | block) & 0xFFFF
    return combine_blocks(plaintext)
