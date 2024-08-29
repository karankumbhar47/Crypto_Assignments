# Generating a Certificate and Private Key with OpenSSL

Following are the instruction for  generating a private key, a Certificate Signing Request (CSR), and a self-signed certificate using OpenSSL.

### 1: Generate the Private Key (`mykey.pem`)

Use the following command to generate a private key:

```bash
openssl genpkey -algorithm RSA -out mykey.pem -aes256
```

- The `-algorithm RSA` option specifies that the RSA algorithm should be used.
- The `-out mykey.pem` option specifies the output file for the private key.
- The `-aes256` option encrypts the private key with AES-256.

You will be prompted to set a passphrase for the key, which adds an extra layer of security.

### 2. Generate a Certificate Signing Request (CSR)

Next, create a Certificate Signing Request (CSR), which is used to generate the certificate. Run the following command:

```bash
openssl req -new -key mykey.pem -out mycsr.csr
```

You will be prompted to provide information such as:
- Country Name (2-letter code)
- State or Province Name
- Locality Name (City)
- Organization Name (Company)
- Organizational Unit Name (Department)
- Common Name (Domain Name)


### 3. Generate the Self-Signed Certificate (`mycert.pem`)

Finally, use the CSR and the private key to create a self-signed certificate:

```bash
openssl x509 -req -days 365 -in mycsr.csr -signkey mykey.pem -out mycert.pem
```
- The `-req` option tells OpenSSL to generate a certificate from the CSR.
- The `-days 365` option specifies that the certificate will be valid for 365 days.
- The `-signkey mykey.pem option tells OpenSSL to sign the certificate with the private key.

This command creates `mycert.pem`(the certificate file) and `mykey.pem` (the private key file).

### 4. Viewing Certificate Information

To inspect the details of the certificate, you can use the following command:

```bash
openssl x509 -in mycert.pem -text -noout
```

This will display information such as the issuer, subject, and validity period of the certificate.
