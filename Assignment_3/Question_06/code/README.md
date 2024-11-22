## How to Run

### Prerequisites
- Python 3.x installed on your system.

### Running the Program
1. Navigate to the `code` directory:
   ```bash
   cd code

2.  Execute the main script:
```bash
    python main.py
```

### Output

- The program will:
    1. Encrypt and decrypt a message using Sypher004.
    2. Apply CBC and CFB modes for encryption and decryption.
    3. Simulate an error during transmission and show how it propagates during decryption.

### File Descriptions

-  `main.py`:
    1. The entry point of the program.
    2. Executes all functionalities, including Sypher004 encryption, CBC/CFB modes, and error simulation.

- `sypher004.py`:
    1. Implements the sypher004_encrypt and sypher004_decrypt functions.
    2. Core logic for substitution and permutation is included.

- `mode.py`:
    1. Contains cbc_encrypt, cbc_decrypt, cfb_encrypt, and cfb_decrypt functions.
    2. Implements both modes of operation using Sypher004.

- `utils.py`:
    -  Provides helper functions:
        1. Message padding.
        2. Initialization vector generation.
        3. Simulating errors by flipping bits in ciphertext blocks.

