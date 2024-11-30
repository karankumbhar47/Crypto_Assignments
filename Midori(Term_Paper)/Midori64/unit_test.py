import unittest
from utils import *
from Midori import *

class Test_Midori64(unittest.TestCase):

    def test_KeyGen(self):
        K0 = "687ded3b3c85b3f3" 
        K1 = "5b1009863e2a8cbf"
        WK = "336de4bd02af3f4c"
        key_128bit = K0+K1
        expected_output = (stringToHexList(WK), stringToHexList(K0), stringToHexList(K1))
        self.assertEqual(expected_output, KeyGen(key_128bit))

 
    def test_KeyAdd(self):
        # Before Round 0
        state = "42c20fd3b586879e"
        WK = "336de4bd02af3f4c"
        iteration = -1
        expected_output = stringToHexList("71afeb6eb729b8d2")
        self.assertEqual(expected_output, KeyAdd(stringToHexList(state), stringToHexList(WK), iteration))

        # Round 0
        K0 = "687ded3b3c85b3f3"
        state = "5f7f71cfcde4c09d"
        expected_output = stringToHexList("37039df5e170737f")
        self.assertEqual(expected_output, KeyAdd(stringToHexList(state), stringToIntList(K0),0))

        #Round 1
        K1 = "5b1009863e2a8cbf"
        state = "37262c922bfeb3c4"
        expected_output = stringToHexList("6d27351404d43f7b")
        self.assertEqual(expected_output, KeyAdd(stringToHexList(state), stringToIntList(K1),1)) 

    def test_SubCell(self):
        # Round 0
        expected_output= "7a1645f457d9582d"
        self.assertEqual(stringToHexList(expected_output), SubCell(stringToHexList("71afeb6eb729b8d2")))

        # Round 1
        expected_output= "37c3926b4a7c7376"
        self.assertEqual(stringToHexList(expected_output), SubCell(stringToHexList("37039df5e170737f")))

        # Round 2
        expected_output= "f2d73baece2e3675"
        self.assertEqual(stringToHexList(expected_output), SubCell(stringToHexList("6d27351404d43f7b")))
 
 
    def test_ShuffleCell(self):
        # Round 0
        expected_output = "7d5d249a765f4815"
        self.assertEqual(stringToHexList(expected_output),ShuffleCell(stringToHexList("7a1645f457d9582d")))

        # Round 1
        expected_output = "372679c7a376b3c4"
        self.assertEqual(stringToHexList(expected_output),ShuffleCell(stringToHexList("37c3926b4a7c7376")))

        # Round 2
        expected_output = "f2b573e2e73ae6dc"
        self.assertEqual(stringToHexList(expected_output),ShuffleCell(stringToHexList("f2d73baece2e3675")))
 
 
    def test_MixColumn(self):
        # Round 0 
        expected_output = "5f7f71cfcde4c09d"
        self.assertEqual(stringToHexList(expected_output), MixColumn(stringToHexList("7d5d249a765f4815")))

        # Round 1
        expected_output = "37262c922bfeb3c4"
        self.assertEqual(stringToHexList(expected_output), MixColumn(stringToHexList("372679c7a376b3c4")))
 
    def test_Midori64_Core(self):
        # Test Cases are obtained from the research paper
        key_128Bit = "00000000000000000000000000000000"
        WK, K0, K1 = KeyGen(key_128Bit)
        expected_output = "3c9cceda2bbd449a"
        plainText = "0000000000000000"
        self.assertEqual(stringToHexList(expected_output),Midori64_Core(plainText, WK, K0, K1))
        
        key_128Bit = "687ded3b3c85b3f35b1009863e2a8cbf"
        WK, K0, K1 = KeyGen(key_128Bit)
        expected_output = "66bcdc6270d901cd"
        plainText = "42c20fd3b586879e"
        self.assertEqual(stringToHexList(expected_output),Midori64_Core(plainText, WK, K0, K1))