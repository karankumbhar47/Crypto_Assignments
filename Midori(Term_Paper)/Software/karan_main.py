import os
import sqlite3
from karan import *
from utils import *
from Midori import *
from getpass import getpass
from pyfzf.pyfzf import FzfPrompt


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


data_fileName = "pass_storage"

try:
    dataDir = os.path.join(os.environ["XDG_DATA_HOME"], data_fileName)
except:
    dataDir = os.path.join(os.environ["HOME"], ".local/share/" + data_fileName)

password_database = os.path.join(dataDir, "pass.db")

try:
    os.makedirs(dataDir, exist_ok=True)
except:
    print(f"Failed to create directory {dataDir}, aborting...")
    exit(1)


conn = sqlite3.connect(password_database)
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
"""
)
conn.commit()


def encrypt(text: str, key: str) -> str:
    ecb = ECBMode(Midori64_Core, Midori64_Core_Decrypt, key)
    return ecb.encrypt_ecb(text)


def decrypt(ciphertext: str, key: str) -> str:
    ecb = ECBMode(Midori64_Core, Midori64_Core_Decrypt, key)
    return ecb.decrypt_ecb(ciphertext)


def generate_key(master_password: str, custom_salt: int = 235230723) -> str:
    custom_salt = custom_salt.to_bytes(16, byteorder="big")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=16,  
        salt=custom_salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = kdf.derive(master_password.encode())

    return key.hex()


def store_password(website: str, username: str, password: str, key: str) -> None:
    encrypted_password = encrypt(password, key)

    cursor.execute(
        "INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
        (website, username, encrypted_password),
    )
    conn.commit()



def retrieve_password(website: str, username: str, key: str) -> str:
    print(f"website: {website}, username: {username}")
    cursor.execute(
        "SELECT id, password FROM passwords WHERE website = ? AND username = ?",
        (website, username),
    )
    result = cursor.fetchone()

    if result:
        id, encrypted_password = result
        decrypted_password = decrypt(encrypted_password, key)
        return decrypted_password
    else:
        return None


def check_master_pass(master_password: str) -> bool:
    cursor.execute('SELECT username, password FROM passwords WHERE website = "$$"')
    result = cursor.fetchone()

    if result is None:
        print("Welcome to PassMonk")

        salt = int.from_bytes(os.urandom(16), byteorder="big") % (10**9)

        if salt == 235230724:
            raise Exception("You are unlucky, try again")

        pass_hash = generate_key(master_password, custom_salt=salt)
        var_pass = getpass("Confirm master password: ")

        if var_pass != master_password:
            print("Two passwords do not match, try again...")
            return False

        cursor.execute(
            'INSERT INTO passwords (website, username, password) VALUES ("$$", ?, ?)',
            (salt, pass_hash),
        )
        conn.commit()
        return True

    
    stored_salt = int(result[0])  
    stored_hash = result[1]

    if stored_hash == generate_key(master_password, custom_salt=stored_salt):
        return True

    return False

def enter_application():
    valid_pass = False
    for _ in range(3):
        master_password = getpass( "Enter master password to Enter the Application: ")
        
        if check_master_pass(master_password):
            valid_pass = True
            break
        else:
            print("Incorrect password")

    if not valid_pass:
        print("Three failed attempts to enter the master password, exiting...")
        return

    return master_password

def main():
    master_password = enter_application()
    key = generate_key(master_password)

    fzf = FzfPrompt()
    actions = fzf.prompt(["Retrieve Password", "Store Password"])

    if not actions:
        print("Action not selected. Exiting.")
        return

    action = actions[0]
    if action == "Store Password":
        website = input("Enter website url: ")
        username = input("Enter your username: ")
        password = getpass("password: ")
        store_password(website, username, password, key)
    elif action == "Retrieve Password":
        cursor.execute("SELECT website FROM passwords")
        result = cursor.fetchall()
        if len(result) == 1:
            print("No stored password found, aborting...")
            return
        website = fzf.prompt([r[0] for r in result if r[0] != "$$"])
        if not website:
            print("Website not selected, aborting...")
            return
        website = website[0]

        cursor.execute("SELECT username FROM passwords WHERE website = ?", ([website]))
        result = cursor.fetchall()
        username = ""
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
        if retrieved_password:
            print(f"Retrieved Password: {retrieved_password}")
        else:
            print("Password not found.")
    else:
        print("Invalid action.")


if __name__ == "__main__":
    main()