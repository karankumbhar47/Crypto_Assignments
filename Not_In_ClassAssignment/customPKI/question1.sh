#!/bin/bash
keyPath=$1
pass=$2

openssl pkeyutl -decrypt -inkey $keyPath -in encrypted_message.bin -passin pass:$pass

# random number is as follows
# 3b4a8385707ecf88f1dcce7d1a28dcfa