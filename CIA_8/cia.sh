#!/bin/bash

# Function to generate the next hash prefix using SHA-256 and OpenSSL
# We only keep the first 10 hex characters (40 bits)
get_hash_prefix() {
    echo -n "$1" | openssl dgst -sha256 | cut -d' ' -f2 | cut -c1-10
}

# Initialize starting points for the Rho method
# Use a random 40-bit initial message (5 bytes)
start_message=$(openssl rand -hex 5)
tortoise="$start_message"
hare="$start_message"

echo "Starting Rho method for SHA-256 40-bit collision detection..."
count=0

while true; do
    # Move the "tortoise" one step (1 hash computation)
    tortoise_hash=$(get_hash_prefix "$tortoise")
    tortoise="$tortoise_hash"

    # Move the "hare" two steps (2 hash computations)
    hare_hash=$(get_hash_prefix "$hare")
    hare=$(get_hash_prefix "$hare_hash")

    ((count++))
    echo "Step $count: No collision found"

    # Check if a collision has been found in the 40-bit prefixes
    if [[ "$tortoise" == "$hare" ]]; then
        echo "Potential cycle detected! Looking for collision messages..."

        # Retrace steps to find the actual collision messages
        tortoise="$start_message"
        while [[ "$tortoise" != "$hare" ]]; do
            tortoise_hash=$(get_hash_prefix "$tortoise")
            hare_hash=$(get_hash_prefix "$hare")

            tortoise="$tortoise_hash"
            hare="$hare_hash"
        done

        echo "Collision found!"
        echo "Message 1 (starting point): $start_message"
        echo "Message 2 (colliding): $tortoise"
        echo "Hash prefix (first 40 bits): $tortoise_hash"
        break
    fi
done
