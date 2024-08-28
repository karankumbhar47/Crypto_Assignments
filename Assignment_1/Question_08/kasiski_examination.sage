# Implementation of kasisiki examination till 

def find_repeated_sequences(ciphertext, seq_length):
    seq_positions = {}
    for i in range(len(ciphertext) - seq_length):
        seq = ciphertext[i:i + seq_length]
        if seq in seq_positions:
            seq_positions[seq].append(i)
        else:
            seq_positions[seq] = [i]
    
    repeated_sequences = {seq: pos for seq, pos in seq_positions.items() if len(pos) > 1}
    
    return repeated_sequences

def gcd_of_distances(positions):
    from math import gcd
    distances = []
    for i in range(len(positions) - 1):
        distances.append(positions[i+1] - positions[i])
    
    gcd_distance = distances[0]
    for d in distances[1:]:
        gcd_distance = gcd(gcd_distance, d)
    
    return gcd_distance

def kasiski_examination(ciphertext):
    seq_length = 2
    while seq_length < len(ciphertext) // 2:
        repeated_sequences = find_repeated_sequences(ciphertext, seq_length)
        
        if repeated_sequences:
 
            gcd_distances = []
            for seq, positions in repeated_sequences.items():
                gcd_distances.append(gcd_of_distances(positions))
            
            keyword_length = gcd_distances[0]
            for g in gcd_distances[1:]:
                keyword_length = gcd(keyword_length, g)
            
            return keyword_length
        
        seq_length += 1

    return None

# Example ciphertext
ciphertext = "NRZATPNRZNRZATP"  # Example ciphertext encoded with 3 length key


keyword_length = kasiski_examination(ciphertext)
print("Estimated Keyword Length: ", keyword_length)

# Further steps would include frequency analysis to determine the actual keyword.
