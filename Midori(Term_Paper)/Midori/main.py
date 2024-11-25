from Midori import *
from utils import *

def main():
    key_128Bit = "687ded3b3c85b3f35b1009863e2a8cbf"
    WK, K0, K1 = KeyGen(key_128Bit)

    plainText = "42c20fd3b586879e"
    expected_output = "66bcdc6270d901cd"

    print("Output from Algorithm: ", *Midori64_Core(plainText, WK, K0, K1))
    print("Expected Output      : ", *stringToHexList(expected_output))


if __name__ == "__main__":
    main()