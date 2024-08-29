# TLS Protocol Testing Script(run.sh)

This script helps you generate a private key, a Certificate Signing Request (CSR), and a self-signed certificate using OpenSSL. It then runs servers and clients for both TLS 1.2 and TLS 1.3 in separate terminal windows, allowing you to observe the handshake processes for each protocol.

## Requirements

- **OpenSSL**: Make sure OpenSSL is installed on your system.
- **GNOME Terminal**: The script requires `gnome-terminal` to open new terminal windows. Ensure that this is available on your system.

## Instructions

### 1. Setup

1. **Create a New Directory**: 
   - It's recommended to run this script in a new, empty directory to avoid conflicts with other files.
   - You can create a directory with:
     ```bash
     mkdir tls_test && cd tls_test
     ```

2. **Copy the Script**: 
   - Save the script (`openssl_test.sh`) into your newly created directory.

3. **Make the Script Executable**:
   - Ensure the script has execute permissions:
     ```bash
     chmod +x openssl_test.sh
     ```

### 2. Running the Script

To execute the script, simply run:

```bash
./openssl_test.sh
```
### 3. What Happens Next?

1. Terminal Windows:
- The script will open four new terminal windows with the following titles:
    - TLS 1.2 Server
    - TLS 1.2 Client
    - TLS 1.3 Server
    - TLS 1.3 Client
- Each server window will prompt you to enter the passphrase for the private key before starting.

2. Server and Client Interaction:
- After entering the passphrase, the server will start and wait for a client connection.
- The corresponding client window will attempt to connect to the server, and you will be able to observe the handshake process.

### 4. Important Notes
- Passphrases: You will be prompted to set a passphrase during the generation of the private key. You will also need to enter this passphrase when starting each server.
- Waiting Periods: The script includes a short delay (sleep 10) to allow the server to start properly before the client attempts to connect. You will be ask for password at starting of the server. **You have to enter this password in 10 sec.* Otherwise client will fail to connect to server.

### 5. Expected Output
- The terminal windows will show the handshake details for each protocol. You should be able to distinguish between the TLS 1.2 and TLS 1.3 inter. What Happens Next?

### 6. Closing Windows
- Once the process is complete, you can close the terminal windows manually.