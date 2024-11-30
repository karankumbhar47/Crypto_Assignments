#!/bin/bash

# Generate and store hash prefixes for SHA-256 to find a 40-bit collision.

# Function to generate a random 40-bit message (5 bytes)
generate_random_message() {
    openssl rand -hex 5
}

# Dictionary to store the hash prefixes
declare -A hash_prefixes
count=0

while true; do
    # Generate a random message
    message=$(generate_random_message)

    # Compute SHA-256 hash, only extracting the first 10 hex chars (40 bits)
    hash_prefix=$(echo -n "$message" | openssl dgst -sha256 | cut -d' ' -f2 | cut -c1-10)

    # Check if this prefix already exists in the dictionary
    if [[ -n ${hash_prefixes[$hash_prefix]} ]]; then
        echo "Collision found!"
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

