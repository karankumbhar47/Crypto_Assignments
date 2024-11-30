#!/bin/bash

# Generate and store hash prefixes for SHA-256 to find a 40-bit collision.

# Function to generate a pseudorandom 5-byte message based on an LFSR polynomial
generate_lfsr_message() {
    local poly=$1
    local reg=0x1F  # Initial state (can be any 5-bit value)
    local message=""

    for (( i=0; i<5; i++ )); do
        byte=0
        for (( j=0; j<8; j++ )); do
            # Compute LFSR feedback using XOR of bits specified by the polynomial
            feedback=0
            for bit in $poly; do
                feedback=$((feedback ^ ((reg >> bit) & 1) ))
            done
            reg=$((( reg << 1 ) | feedback ))  # Shift left and add feedback to LSB

            byte=$((( byte << 1 ) | ( reg & 1 )))
        done
        message+=$(printf "%02x" "$byte")
    done
    echo "$message"

}

# List of polynomials (bit positions for feedback)
declare -A polynomials=(
    ["poly1"]="4 1"             # x^5 + x^2 + 1
    ["poly2"]="4 2 0"           # x^5 + x^3 + x + 1
    ["poly3"]="4 3"             # x^5 + x^4 + 1
    ["poly4"]="4 3 1 0"         # x^5 + x^4 + x^2 + x + 1
    ["poly5"]="4 3 2 1"         # x^5 + x^4 + x^3 + x^2 + 1
)

# Dictionary to store the hash prefixes and messages
declare -A hash_prefixes
count=0
# Loop through each polynomial
for poly_name in "${!polynomials[@]}"; do
    poly="${polynomials[$poly_name]}"
    echo "Using polynomial: $poly_name"

    while true; do
        # Generate a message using the LFSR
        message=$(generate_lfsr_message "$poly")

        # Compute SHA-256 hash, only extracting the first 10 hex chars (40 bits)
        hash_prefix=$(echo -n "$message" | openssl dgst -sha256 | cut -d' ' -f2 | cut -c1-10)

        # Check if this prefix already exists in the dictionary
        if [[ -n ${hash_prefixes[$hash_prefix]} ]]; then
            echo "Collision found for polynomial $poly_name!"
            echo "Message 1: ${hash_prefixes[$hash_prefix]}"
            echo "Message 2: $message"
            echo "Hash prefix (first 40 bits): $hash_prefix"
            break
        else
            # Store the message with the hash prefix as the key
            hash_prefixes[$hash_prefix]=$message
            echo "Collision Not Found: $count"
            ((count++))
        fi
    done
done
