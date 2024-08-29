# Capture The Flag Solution

This repository contains the solution for the Capture The Flag (CTF) assignment. The primary task is to decrypt a given ciphertext to reveal hidden links". 

## Overview

The provided scripts are designed to:
1. Convert ciphertext to ASCII values.
2. Identify patterns in the ciphertext.
3. Guess the encryption key based on identified patterns.
4. Decrypt the ciphertext to reveal potential links.

## Files Included

- `attack.py`: The main script to run the attack.
- `ascii.py`: Contains functions to convert ciphertext to ASCII and find patterns.
- `utils.py`: Provides utility functions for key guessing, encryption, and decryption.

## Prerequisites

Ensure you have Python installed. The scripts are compatible with Python 3.x.

## How to Run

1. **`cipherText.txt`:**
   - Ensure you have a `cipherText.txt` file in the same directory as `attack.py`. This file should contain the ciphertext with red and black colored text separated by new lines.

2. **Run the Attack Script:**
   - Execute `attack.py` using the following command:

     ```bash
     python attack.py
     ```

   - This script will:
     - Convert the ciphertext to ASCII values using `chipherToAscii()` from `ascii.py`.
     - Find potential key patterns using `getPatternIndex()` from `ascii.py`.
     - Generate and test possible keys to decrypt the ciphertext.
     - Print possible keys and decrypted links to the terminal.

3. **Review Output:**
   - The script will output potential keys and decrypted links. Review these links to identify the correct one.

## Functions

### `ascii.py`

- **`chipherToAscii()`**: Converts the ciphertext to ASCII values.
- **`getPatternIndex(cipherText)`**: Finds indices where the ciphertext matches a specific pattern.

### `utils.py`

- **`tryAllKey(m, target)`**: Tests all possible keys to match a given target value.
- **`getKey(pair, keys)`**: Refines key guesses based on ciphertext and message pairs.
- **`decrypt(c, keys)`**: Decrypts a single character of ciphertext using the provided key.
- **`encrypt(m, keys)`**: Encrypts a single character using the provided key (not used in `attack.py`).
- **`getLink(cipherText, keys)`**: Decrypts the entire ciphertext to find the link.

## Note

- Ensure all Python scripts (`attack.py`, `ascii.py`, `utils.py`) and the `cipherText.txt` file are located in the same directory.
