#!/bin/bash

# Directory to store output files
OUTPUT_DIR="./tls_dumps"
mkdir -p $OUTPUT_DIR

# Server and client certificates (self-signed for testing)
CERT_FILE="../mycert.pem"
KEY_FILE="../mykey.pem"

# Generate certificates if they don't exist
if [[ ! -f "$CERT_FILE" || ! -f "$KEY_FILE" ]]; then
  openssl req -x509 -newkey rsa:4096 -keyout $KEY_FILE -out $CERT_FILE -days 365 -nodes -subj "/CN=localhost"
fi

# Start OpenSSL server in the background
start_server() {
  local protocol=$1
  local port=$2

  echo "Starting OpenSSL server with $protocol on port $port..."
  openssl s_server -accept $port -cert $CERT_FILE -key $KEY_FILE -$protocol &
  SERVER_PID=$!
  sleep 12 # Give server time to start
}

# Capture TLS handshake using OpenSSL client
capture_handshake() {
  local protocol=$1
  local port=$2
  local output_file=$3

  echo "Capturing handshake with $protocol..."
  echo | openssl s_client -connect localhost:$port -$protocol >$output_file 2>&1
}

# Kill the server process
kill_server() {
  kill $SERVER_PID
}

# TLS 1.2
start_server "tls1_2" 4433
capture_handshake "tls1_2" 4433 "$OUTPUT_DIR/tls12_dump.txt"
kill_server

# TLS 1.3
start_server "tls1_3" 4434
capture_handshake "tls1_3" 4434 "$OUTPUT_DIR/tls13_dump.txt"
kill_server

echo "Comparison files generated in $OUTPUT_DIR."
