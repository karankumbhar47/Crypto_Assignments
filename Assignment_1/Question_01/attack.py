import ascii 
import utils 

startMessage = "https://drive.google.com/drive"

cipherText = ascii.chipherToAscii()
guessIndex = ascii.getPatternIndex(cipherText)

for index in guessIndex:
    pair = []
    for i,s in enumerate(startMessage):
        pair.append((ord(s),cipherText[index+i]))
         
    keys = utils.tryAllKey(pair[0][0],pair[0][1])
    final_key = utils.getKey(pair,keys)
    print("Key --> ",final_key)
    print("Link --> ",utils.getLink(cipherText[index:],final_key[0]))

