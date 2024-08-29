# Examining a TLS Handshake Using OpenSSL

### 1. Start the OpenSSL Server

Use the `openssl s_server` command to start a simple TLS/SSL server. Specify the protocol version, private key, and certificate.

To start a server using **TLS 1.2**:

```bash
openssl s_server -cert mycert.pem -key mykey.pem -accept 4433 -tls1_2
```

For **TLS 1.3** :

```bash
openssl s_server -cert mycert.pem -key mykey.pem -accept 4433 -tls1_3
```
Replace mycert.pem and mykey.pem with certificate and private key files generated through the instruction of    [CreateKey.md](./CreateKey.md) file.

### 2. Connect to the Server with OpenSSL Client

In another terminal, use the openssl s_client command to connect to the server. This will initiate the handshake and allow you to observe it.

For **TLS 1.2**:

```bash
openssl s_client -connect localhost:4433 -tls1_2
```

For **TLS 1.3**:

```bash
openssl s_client -connect localhost:4433 -tls1_3
```

The client will output details of the handshake, including the protocol, cipher suite, and certificates exchanged.

### 3. Examine the Handshake Output

The output of the openssl s_client command will show the steps of the handshake:

- **Protocol**: Indicates whether TLS 1.2 or TLS 1.3 is used.
- **Cipher**: The negotiated cipher suite.
- **Certificate**: Information about the server’s certificate, including the subject, issuer, and validity period.
- **Key Exchange**: Details about the key exchange mechanism (e.g., RSA for TLS 1.2 or ECDHE for TLS 1.3).
- **Handshake Messages**: Displays the process of exchanging messages between the client and server.