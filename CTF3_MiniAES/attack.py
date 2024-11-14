from utils import *
from miniAES import encrypt
from miniAESDecrypt import decrypt

def create_attack_plaintexts(base_nibbles, varying_idx=0):
    plain_data = []
    for val in range(16):
        modified_nibbles = base_nibbles[:]
        modified_nibbles[varying_idx] = val
        plain_data.append([n for n in modified_nibbles])
    return plain_data

def perform_square_attack(cipher_blocks, nib_pos):
    possible_keys = []

    for guess1 in range(16):
        for guess2 in range(16):
            checksum = [0, 0, 0, 0]

            for block in cipher_blocks:
                
                last_key_guess = [0, 0, 0, 0]
                last_key_guess[nib_pos] = guess2

                state = apply_round_key(block, last_key_guess)
                state = reverse_row_shift(state)
                state = inverse_substitute(state)

                second_last_key_guess = [0, 0, 0, 0]
                if nib_pos % 2 == 0:  
                    second_last_key_guess[nib_pos] = guess1
                else:  
                    second_last_key_guess[(nib_pos+2)%4] = guess1

                state = apply_round_key(state, second_last_key_guess)
                state = inv_mix_columns(state)
                state = reverse_row_shift(state)
                state = inverse_substitute(state)

                for idx in range(4):
                    checksum[idx] ^= state[idx]

            if checksum[nib_pos] == 0:
                possible_keys.append(guess2)

    return possible_keys

def generate_key_candidates(list1, list2, list3, list4):
    unique1, unique2, unique3, unique4 = map(set, (list1, list2, list3, list4))
    all_keys = []
    for a in unique1:
        for b in unique2:
            for c in unique3:
                for d in unique4:
                    all_keys.append([a, b, c, d])
    return all_keys

def main():
    fixed_base = [0x0, 0x2, 0x1, 0x9]  
    plain_blocks = create_attack_plaintexts(fixed_base, 0)

    encrypted_blocks = []
    for block in plain_blocks:
        cipher_block = oracle_encrypt("./oracle", block)
        encrypted_blocks.append(cipher_block)

    nibble_results = []
    for idx in range(4):
        nibble_results.append(perform_square_attack(encrypted_blocks, idx))

    key_candidates = generate_key_candidates(*nibble_results)
    derived_keys = [reverse_key_schedule(k) for k in key_candidates]

    potential_master_keys = []
    for key in derived_keys:
        if oracle_encrypt("./oracle", [1, 2, 3, 4]) == encrypt([1, 2, 3, 4], key):
            potential_master_keys.append([int(elem) for elem in key])

    with open('ciphertext.txt', 'r') as file:
        cipher_text_hex = file.readline().strip()

    cipher_data_blocks = [cipher_text_hex[i:i+4] for i in range(0, len(cipher_text_hex), 4)]
    cipher_data_blocks = [[int(cipher_data_blocks[b][j:j+1], 16) for j in range(4)] for b in range(len(cipher_data_blocks))]

    for key in potential_master_keys:
        decoded_blocks = [decrypt(block, key) for block in cipher_data_blocks]
        plain_text_hex = ''.join([''.join([hex(nib)[2:] for nib in block]) for block in decoded_blocks])

        hex_text = plain_text_hex
        ascii_output = [chr(int(hex_text[i:i+2], 16)) for i in range(0, len(hex_text), 2)]
        extracted_url = ''.join(ascii_output)

        if extracted_url.startswith('https'):
            print("Original Link:", extracted_url)
            break

if __name__=="__main__":
    main()