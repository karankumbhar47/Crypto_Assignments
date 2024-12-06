import os
import sqlite3

from Midori import *
from utils import *
from getpass import getpass
from base64 import b64encode

from pyfzf.pyfzf import FzfPrompt

####################################### DATABASE INITIALIZATION ##################################################
try:
    dataDir = os.path.join(os.environ["XDG_DATA_HOME"], "passmonk")
except:
    dataDir = os.path.join(os.environ["HOME"], ".local/share/passmonk")
passFile = os.path.join(dataDir, "passwords.db")
try:
    os.makedirs(dataDir, exist_ok=True)
except:
    print(f"Failed to create directory {dataDir}, aborting...")
    exit(1)

conn = sqlite3.connect(passFile)
cursor = conn.cursor()

###################################### CREATE THE TABLE IF IT DOESN'T EXIST ######################################
cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

def encrypt(text: str, key: str) -> bytes:
    ############################## Generate a random IV (Initialization Vector) ###################################
    iv = os.urandom(16)

    #################################### PAD THE PLAINTEXT BEFORE ENCRYPTION ######################################
    pad_length = (16 - (len(text) % 16)) % 16
    padded_text = text + (chr(pad_length) * pad_length)

    ######################## CREATE THE CIPHER OBJECT WITH MIDORI AND THE GENERATED IV ###########################
    WK, K0, K1 = KeyGen(key)
    ciphertext = b"".join([bytes(Midori64_Core(padded_text[i:i + 16], WK, K0, K1)) for i in range(0, len(padded_text), 16)])

    ############################# RETURN THE IV CONCATENATED WITH THE CIPHERTEXT ##################################
    return iv + ciphertext

def decrypt(ciphertext: bytes, key: str) -> str:
    ########################### EXTRACT THE IV FROM THE FIRST 16 BYTES OF THE CIPHERTEXT ##########################
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]

    ######################### CREATE THE CIPHER OBJECT WITH MIDORI AND THE EXTRACTED IV ###########################
    WK, K0, K1 = KeyGen(key)
    decrypted_blocks = [Midori64_Core_Decrypt(ciphertext[i:i + 16], WK, K0, K1) for i in range(0, len(ciphertext), 16)]
    decrypted_data = b"".join(decrypted_blocks)

    ######################################### UNPAD THE DECRYPTED DATA ############################################
    pad_length = decrypted_data[-1]
    if pad_length < 1 or pad_length > 16:
        return "Invalid Master Password."
    return decrypted_data[:-pad_length].decode()

################################################## GENERATING KEY #################################################
def generate_key(master_password: str, salt: bytes = bytes(235230723)) -> str:
    hashed_key = master_password.encode() + salt
    return hashed_key[:16].hex()  # Midori uses 128-bit (16 bytes) keys in hex format

########################################## FUNCTION FOR STORING PASSWORD ##########################################
def store_password(website: str, username: str, password: str, key: str) -> None:
    ########################################## GENERATE A RANDOM SALT #############################################
    salt = os.urandom(16)
    encrypted_password = encrypt(password, key)

    cursor.execute('INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)', (website, username, encrypted_password))
    conn.commit()

########################################### FUNCTION FOR GETTING PASSWORD ##########################################
def retrieve_password(website: str, username: str, key: str) -> str:
    print(f"website: {website}, username: {username}")
    cursor.execute('SELECT id, password FROM passwords WHERE website = ? AND username = ?', (website, username))
    result = cursor.fetchone()

    if result:
        id, encrypted_password = result
        decrypted_password = decrypt(encrypted_password, key)
        return decrypted_password
    else:
        return None

def check_master_pass(master_password: str) -> bool:
    cursor.execute('SELECT username,password FROM passwords WHERE website = "$$"')
    result = cursor.fetchone()
    if result is None:
        # This is being run for first time
        print("Welcome to PassMonk")
        salt = os.urandom(16)
        pass_hash = generate_key(master_password, salt)

        var_pass = getpass("Confirm master password: ")
        if var_pass != master_password:
            print("Two passwords do not match, try again...")
            return False

        cursor.execute('INSERT INTO passwords (website, username, password) VALUES ("$$", ?, ?)', (salt, b64encode(pass_hash.encode()).decode()))
        conn.commit()
        return True

    if result[1] == b64encode(generate_key(master_password, result[0]).encode()).decode():
        return True
    return False

def main():

    # Get the password
    valid_pass = False
    for _ in range(3):
        master_password = getpass("Enter master password to access the password store: ")
        # Verify the key using some method and throw error if it is wrong
        if check_master_pass(master_password):
            valid_pass = True
            break
        else:
            print("Incorrect password")
    if not valid_pass:
        print("Three failed attempts to enter the master password, exiting...")
        return

    key = generate_key(master_password)

    fzf = FzfPrompt()
    actions = fzf.prompt(['Retrieve Password', 'Store Password'])

    if not actions:
        print("Action not selected. Exiting.")
        return

    action = actions[0]
    if action == 'Store Password':
        website = input("Enter website: ")
        username = input("Enter username: ")
        password = getpass("Enter password: ")
        hashed_key = password.encode()
        password = hashed_key[:16].hex()  # Midori uses 128-bit (16 bytes) keys in hex format
        store_password(website, username, password, key)
    elif action == 'Retrieve Password':
        cursor.execute('SELECT website FROM passwords')
        result = cursor.fetchall()
        if len(result) == 1:
            print("No stored password found, aborting...")
            return
        website = fzf.prompt([r[0] for r in result if r[0] != "$$"])
        if not website:
            print("Website not selected, aborting...")
            return
        website = website[0]

        cursor.execute('SELECT username FROM passwords WHERE website = ?', ([website]))
        result = cursor.fetchall()
        username = ''
        if len(result) == 1:
            username = result[0][0]
            print(f"Username: {username}")
        elif len(result) == 0:
            raise Exception("Something went wrong...")
        else:
            username = fzf.prompt([r[0] for r in result], "--height ~40%")
            if not username:
                print("Username not selected, aborting...")
                return
            username = username[0]

        retrieved_password = retrieve_password(website, username, key)
        original_bytes = bytes.fromhex(retrieve_password)
    
        retrieve_password = original_bytes.decode('utf-8')
        if retrieved_password:
            print(f"Retrieved Password: {retrieved_password}")
        else:
            print("Password not found.")
    else:
        print("Invalid action.")

if __name__ == "__main__":
    main()
