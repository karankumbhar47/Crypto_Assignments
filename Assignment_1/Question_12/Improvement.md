### Note: TLS 1.3 Improvements Over TLS 1.2

#### TLS 1.3 introduces significant improvements over TLS 1.2, enhancing both security and performance. 
**The key improvements are as follows:**
- Simplified Handshake:
    - TLS 1.3 reduces the number of round trips required for a handshake, enabling a 
    faster connection setup. It can perform a full handshake in a single round trip 
    (1-RTT) compared to TLS 1.2, which requires two round trips (2-RTT).

    - TLS 1.3 also supports "0-RTT" handshakes, allowing clients to send encrypted   
    data with the first handshake message, reducing latency even further.

- Enhanced Security:
    - In TLS 1.3, only five strong cipher suites are supported, eliminating weaker 
    and obsolete cryptographic algorithms, such as SHA-1 and MD5.

    - Forward secrecy is mandatory in TLS 1.3, ensuring that past communications   
    cannot be decrypted even if the server's private key is compromised in the 
    future.

    - The protocol removes support for RSA key exchanges, which were vulnerable to 
    certain attacks in TLS 1.2, and instead uses Diffie-Hellman and Elliptic Curve 
    Diffie-Hellman (ECDHE) as the key exchange mechanisms.

- Simplified Protocol:
    - TLS 1.3 simplifies the protocol by removing outdated features, such as 
    compression, renegotiation, and non-AEAD ciphers (e.g., CBC modes), which were 
    prone to various attacks like BEAST, CRIME, and POODLE.

    - The session resumption mechanism has been replaced with a more secure and 
    efficient Pre-Shared Key (PSK) approach.

- Improved Privacy:
    - TLS 1.3 encrypts more of the handshake process, including the server's 
    certificate, providing better privacy for the connection setup and reducing the 
    potential for passive monitoring and attacks.

These improvements in TLS 1.3 make it more secure, faster, and simpler compared to TLS 
1.2, making it the preferred choice for modern secure communications.
