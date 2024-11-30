#!/bin/bash

# Function to generate a random message of 40 bits
generate_random_message() {
    echo $(openssl rand -hex 5)
}

# Dictionary to store hash prefixes
declare -A hash_prefixes

while true; do
    # Generate a random message
    message=$(generate_random_message)

    # Compute SHA-256 hash and extract the first 10 hex characters (40 bits)
    hash=$(echo -n "$message" | openssl dgst -sha256 | awk '{print $2}')
    hash_prefix=${hash:0:10}

    # Check if this prefix already exists in the dictionary
    if [[ -n ${hash_prefixes[$hash_prefix]} ]]; then
        echo "Collision found!"
        echo "Message 1: ${hash_prefixes[$hash_prefix]}"
        echo "Message 2: $message"
        echo "Hash prefix (first 40 bits): $hash_prefix"
        break
    else
        # Store the message in the dictionary with the hash prefix as the key
        hash_prefixes[$hash_prefix]=$message
    fi
done
