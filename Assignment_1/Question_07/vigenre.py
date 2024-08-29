import time
from tqdm import tqdm
from spellchecker import SpellChecker


def generate_keys():
    keys = []
    for i in range(26):
        key = chr(i+65)+"ACK" 
        keys.append(key)
    for i in range(26):
        key = "A"+chr(i+65)+"CK" 
        keys.append(key)
    return keys

def validateWord(word):
    spell = SpellChecker()
    return word.lower() in spell

def vignere_decrypt(cipherText, key):
    decrypted_text = []
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    cipherText_int = [ord(i) for i in cipherText]
    
    for i in range(len(cipherText_int)):
        value = (cipherText_int[i] - key_as_int[i % key_length]) % 26
        decrypted_text.append(chr(value + 65)) 

    return ''.join(decrypted_text)

def validate_key(plainText):
    if(plainText[0]==plainText[8] and plainText[2]=='F' and plainText[3]=='O'):
        return True
    return False

def find_key(cipherText):
    dictPlainTextKey = {}
    all_keys = generate_keys()
    for key in tqdm(all_keys, desc=f"Trying keys ..."):
        plainText = vignere_decrypt(cipherText,key)
        if(validate_key(plainText)):
            dictPlainTextKey[key] = plainText

        time.sleep(0.1)
    return dictPlainTextKey

def main():
    cipherText = "JNHYSMCDJOP"
    dictKeys = find_key(cipherText)
    print("\nAll Posible Keys: \n")
    for key,value in dictKeys.items():
        if(validateWord(value)):
            print(f"{key} ==> {value} ==> Valid English Word")
        else:
            print(f"{key} ==> {value}")


if __name__=="__main__":
    main()