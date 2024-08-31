#!/bin/bash

openssl pkeyutl -decrypt -inkey 8.key -in encrypted_message.bin -passin pass:***********
