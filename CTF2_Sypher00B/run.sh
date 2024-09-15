for i in {0..31}; do
    ./oracle08 $i 
done >out.txt

# Extract plaintext and ciphertext from out.txt
echo "Ciphertexts:"
grep "Ciphertext" out.txt | awk '{print $2}' | sed 's/Ciphertext: //' | sed 's/^0//' | tr '\n' ',' | sed 's/,$//' | sed 's/^/[/' | sed 's/$/]/'
