#!/bin/bash

openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt

# Start TLS 1.2 server
openssl s_server -cert server.crt -key server.key -www -tls1_2 &
SERVER_PID=$!

# Connect using TLS 1.2
echo "Testing TLS 1.2"
openssl s_client -connect localhost:4433 -tls1_2 >tls1_2_output.txt

# Kill the server
kill $SERVER_PID

# Start TLS 1.3 server
openssl s_server -cert server.crt -key server.key -www -tls1_3 &
SERVER_PID=$!

# Connect using TLS 1.3
echo "Testing TLS 1.3"
openssl s_client -connect localhost:4433 -tls1_3 >tls1_3_output.txt

# Kill the server
kill $SERVER_PID

echo "Done. Outputs are saved in tls1_2_output.txt and tls1_3_output.txt."
