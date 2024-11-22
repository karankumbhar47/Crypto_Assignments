def apply_permutation(input_bits: int, box: list[int]) -> int:
    permuted_bits = 0
    for i in range(16):
        bit = (input_bits >> i) & 1
        permuted_bits |= (bit << box[i])
    return permuted_bits


def split_into_blocks(message: bytes, block_size=2) -> list[int]:
    # padding_length = block_size - (len(message) % block_size)
    padding_length = (block_size - (len(message) % block_size)) % block_size
    message = message+ bytes([padding_length] * padding_length)  # PKCS7 padding
    blocks = [int.from_bytes(message[i:i + block_size], 'big')
              for i in range(0, len(message), block_size)]
    return blocks


def combine_blocks(blocks: list[int], block_size=2) -> bytes:
    return b''.join(block.to_bytes(block_size, 'big') for block in blocks)


def xor(a: int, b: int) -> int:
    return a ^ b


def flip_bit(ciphertext: list[int], block_index: int, bit_position: int) -> list[int]:
    modified_ciphertext = ciphertext[:]
    modified_ciphertext[block_index] ^= (1 << bit_position)
    return modified_ciphertext
