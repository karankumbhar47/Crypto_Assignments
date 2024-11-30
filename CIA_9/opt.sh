#!/bin/bash

generate_random_message() {
    openssl rand -hex 5
}

declare -A hash_prefixes

while true; do
    message=$(generate_random_message)

    hash_prefix=$(echo -n "$message" | openssl dgst -sha256 | cut -d' ' -f2 | cut -c1-10)

    if [[ -n ${hash_prefixes[$hash_prefix]} ]]; then
        echo "Collision found!"
        echo "Message 1: ${hash_prefixes[$hash_prefix]}"
        echo "Message 2: $message"
        echo "Hash prefix (first 40 bits): $hash_prefix"
        break
    else
        hash_prefixes[$hash_prefix]=$message
    fi
done
