import os
import subprocess
import binascii

def sha256_first_40_bits(message):
    """Compute the SHA-256 hash of the message and return the first 40 bits."""
    result = subprocess.run(
        ["echo", "-n", message, "|", "openssl", "dgst", "-sha256"],
        capture_output=True, text=True, shell=True
    )
    hash_hex = result.stdout.split()[-1]  # Extract the hash value from the output
    return hash_hex[:10]  # First 10 hex characters == 40 bits

def find_collision():
    """Finds a collision in the first 40 bits of SHA-256."""
    seen_hashes = {}
    
    while True:
        # Generate a random 40-bit message in hex
        message = binascii.hexlify(os.urandom(5)).decode('utf-8')
        
        # Get the first 40 bits of its SHA-256 hash
        hash_40 = sha256_first_40_bits(message)
        
        # Check for collision
        if hash_40 in seen_hashes:
            print("Collision found!")
            print("Message 1:", seen_hashes[hash_40])
            print("Message 2:", message)
            print("First 40 bits of SHA-256:", hash_40)
            return seen_hashes[hash_40], message
        
        # Store the hash in the dictionary
        seen_hashes[hash_40] = message

# Run the function to find a collision
find_collision()
