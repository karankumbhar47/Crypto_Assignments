## AES 2 Round 

### Overview
1. `Utils.py` 
    - This File contains function that will dump the latex code into `.tex` file.
    - This File Also contains function that will print output in formatted way.
    - Function that will calculate xor of two hex messages.
    - GF2 multiplication of two hex numbers. 
    
2. `AES_2Round.py`
    - This file contains implementation of AES 2 Round implementation.
    - This implementation will use key that we will get from first problem.
    - Also, `main` function that will iterate AES 2 round function with different location from (0,0) to (3,3)
    - Print the output that will show xor variation of different intermediate state of AES 2 round

### How Run the file
1. Change the current directory to the Question_04 directory.
```bash
cd Question_04
```
2. Run the python file

```bash
python AES_2Round.py
```

3. Observer the Output

```bash
location 0,0

Message 1 :  c206281352f0a6b686ca2d3e4dbf43f7
Message 2 :  ff06281352f0a6b686ca2d3e4dbf43f7
Cipher  1 :  437bd144aea476789016b70fe9c9a092
Cipher  2 :  fe7bd144aea476609016bc0fe9a1a092

Xor Variation

Message                 :  3d000000000000000000000000000000
Round Key Apply         :  3d000000000000000000000000000000
First Round Sub         :  8a000000000000000000000000000000
First Round Shift       :  8a000000000000000000000000000000
First Round Mix Col     :  0f0000008a0000008a00000085000000
First Round Key Apply   :  0f0000008a0000008a00000085000000
Second Round Sub        :  bd000000180000000b00000068000000
Second Round Shift      :  bd0000000000001800000b0000680000
Second Round Key Apply  :  bd0000000000001800000b0000680000
CipherText              :  bd0000000000001800000b0000680000

Cipher Diff
[(0, '43', 'fe'), (7, '78', '60'), (10, 'b7', 'bc'), (13, 'c9', 'a1')]

============================================================

location 0,1

Message 1 :  56e9fb027beafdb8f3880bf4b83ffb46
Message 2 :  56fffb027beafdb8f3880bf4b83ffb46
Cipher  1 :  3b7f195d4f582c0781aa0ea884ed411a
Cipher  2 :  3bc7195da6582c0781aa0ed284ed641a

Xor Variation

Message                 :  00160000000000000000000000000000
Round Key Apply         :  00160000000000000000000000000000
First Round Sub         :  00c40000000000000000000000000000
First Round Shift       :  00c40000000000000000000000000000
First Round Mix Col     :  0093000000c4000000c4000000570000
First Round Key Apply   :  0093000000c4000000c4000000570000
Second Round Sub        :  00b8000000e90000007a000000250000
Second Round Shift      :  00b80000e90000000000007a00002500
Second Round Key Apply  :  00b80000e90000000000007a00002500
CipherText              :  00b80000e90000000000007a00002500

Cipher Diff
[(1, '7f', 'c7'), (4, '4f', 'a6'), (11, 'a8', 'd2'), (14, '41', '64')]

============================================================

location 0,2

Message 1 :  31195d65d9165527b60d57c0934cd7c5
Message 2 :  3119ff65d9165527b60d57c0934cd7c5
Cipher  1 :  848841c6ecb22d7bf656f41b124037e7
Cipher  2 :  848879c6ecd92d7b5a56f41b12403794

Xor Variation

Message                 :  0000a200000000000000000000000000
Round Key Apply         :  0000a200000000000000000000000000
First Round Sub         :  00003000000000000000000000000000
First Round Shift       :  00003000000000000000000000000000
First Round Mix Col     :  00006000000030000000300000005000
First Round Key Apply   :  00006000000030000000300000005000
Second Round Sub        :  0000380000006b000000ac0000007300
Second Round Shift      :  00003800006b0000ac00000000000073
Second Round Key Apply  :  00003800006b0000ac00000000000073
CipherText              :  00003800006b0000ac00000000000073

Cipher Diff
[(2, '41', '79'), (5, 'b2', 'd9'), (8, 'f6', '5a'), (15, 'e7', '94')]

============================================================

location 0,3

Message 1 :  6681b7a5a8eba428209bbcd38b2e4cf6
Message 2 :  6681b7ffa8eba428209bbcd38b2e4cf6
Cipher  1 :  7f688031f97409cb3c448fed918edec1
Cipher  2 :  7f6880d9f97440cb3cd08fed408edec1

Xor Variation

Message                 :  0000005a000000000000000000000000
Round Key Apply         :  0000005a000000000000000000000000
First Round Sub         :  0000006a000000000000000000000000
First Round Shift       :  0000006a000000000000000000000000
First Round Mix Col     :  000000d40000006a0000006a000000be
First Round Key Apply   :  000000d40000006a0000006a000000be
Second Round Sub        :  000000e80000004900000094000000d1
Second Round Shift      :  000000e80000490000940000d1000000
Second Round Key Apply  :  000000e80000490000940000d1000000
CipherText              :  000000e80000490000940000d1000000

Cipher Diff
[(3, '31', 'd9'), (6, '09', '40'), (9, '44', 'd0'), (12, '91', '40')]

============================================================

location 1,0

Message 1 :  39de6fde88610d9a7998a798caae9368
Message 2 :  39de6fdeff610d9a7998a798caae9368
Cipher  1 :  18b981fd6a48e01f3a805092603a0963
Cipher  2 :  18b9811a6a48721f3a895092573a0963

Xor Variation

Message                 :  00000000770000000000000000000000
Round Key Apply         :  00000000770000000000000000000000
First Round Sub         :  00000000270000000000000000000000
First Round Shift       :  00000000000000270000000000000000
First Round Mix Col     :  000000690000004e0000002700000027
First Round Key Apply   :  000000690000004e0000002700000027
Second Round Sub        :  000000e7000000920000000900000037
Second Round Shift      :  000000e7000092000009000037000000
Second Round Key Apply  :  000000e7000092000009000037000000
CipherText              :  000000e7000092000009000037000000

Cipher Diff
[(3, 'fd', '1a'), (6, 'e0', '72'), (9, '80', '89'), (12, '60', '57')]

============================================================

location 1,1

Message 1 :  662c58619eb82fa14120dded8ae103c8
Message 2 :  662c58619eff2fa14120dded8ae103c8
Cipher  1 :  0d3349adfa60e6d15485c72101d2a2c9
Cipher  2 :  e63349adfa60e6fe5485ac2101b2a2c9

Xor Variation

Message                 :  00000000004700000000000000000000
Round Key Apply         :  00000000004700000000000000000000
First Round Sub         :  0000000000f000000000000000000000
First Round Shift       :  00000000f00000000000000000000000
First Round Mix Col     :  0b000000fb000000f0000000f0000000
First Round Key Apply   :  0b000000fb000000f0000000f0000000
Second Round Sub        :  eb0000002f0000006b00000060000000
Second Round Shift      :  eb0000000000002f00006b0000600000
Second Round Key Apply  :  eb0000000000002f00006b0000600000
CipherText              :  eb0000000000002f00006b0000600000

Cipher Diff
[(0, '0d', 'e6'), (7, 'd1', 'fe'), (10, 'c7', 'ac'), (13, 'd2', 'b2')]

============================================================

location 1,2

Message 1 :  a56b8184ac146b48aaaf33416dd27764
Message 2 :  a56b8184ac14ff48aaaf33416dd27764
Cipher  1 :  98e7e0137b9b1ababe590a2d461714ab
Cipher  2 :  98cde0137a9b1ababe590a4446175bab

Xor Variation

Message                 :  00000000000094000000000000000000
Round Key Apply         :  00000000000094000000000000000000
First Round Sub         :  000000000000ee000000000000000000
First Round Shift       :  0000000000ee00000000000000000000
First Round Mix Col     :  0029000000c7000000ee000000ee0000
First Round Key Apply   :  0029000000c7000000ee000000ee0000
Second Round Sub        :  002a00000001000000690000004f0000
Second Round Shift      :  002a0000010000000000006900004f00
Second Round Key Apply  :  002a0000010000000000006900004f00
CipherText              :  002a0000010000000000006900004f00

Cipher Diff
[(1, 'e7', 'cd'), (4, '7b', '7a'), (11, '2d', '44'), (14, '14', '5b')]

============================================================

location 1,3

Message 1 :  4bbc6788f49bb20753ff5912af95bb36
Message 2 :  4bbc6788f49bb2ff53ff5912af95bb36
Cipher  1 :  f982251579d30d301702bf5160e114b1
Cipher  2 :  f9823a1579bd0d301502bf5160e114ef

Xor Variation

Message                 :  00000000000000f80000000000000000
Round Key Apply         :  00000000000000f80000000000000000
First Round Sub         :  000000000000004f0000000000000000
First Round Shift       :  0000000000004f000000000000000000
First Round Mix Col     :  0000d10000009e0000004f0000004f00
First Round Key Apply   :  0000d10000009e0000004f0000004f00
Second Round Sub        :  00001f0000006e000000020000005e00
Second Round Shift      :  00001f00006e0000020000000000005e
Second Round Key Apply  :  00001f00006e0000020000000000005e
CipherText              :  00001f00006e0000020000000000005e

Cipher Diff
[(2, '25', '3a'), (5, 'd3', 'bd'), (8, '17', '15'), (15, 'b1', 'ef')]

============================================================

location 2,0

Message 1 :  cb12bcfce9822cacff9caf3c866c1d4f
Message 2 :  cb12bcfce9822cacff9caf3c866c1d4f
Cipher  1 :  58bb88cc71df4a148f07eaf45323ac0e
Cipher  2 :  58bb88cc71df4a148f07eaf45323ac0e

Xor Variation

Message                 :  00000000000000000000000000000000
Round Key Apply         :  00000000000000000000000000000000
First Round Sub         :  00000000000000000000000000000000
First Round Shift       :  00000000000000000000000000000000
First Round Mix Col     :  00000000000000000000000000000000
First Round Key Apply   :  00000000000000000000000000000000
Second Round Sub        :  00000000000000000000000000000000
Second Round Shift      :  00000000000000000000000000000000
Second Round Key Apply  :  00000000000000000000000000000000
CipherText              :  00000000000000000000000000000000

Cipher Diff
[]

============================================================

location 2,1

Message 1 :  dc84a3e4e5700a9781831c087ffdc059
Message 2 :  dc84a3e4e5700a9781ff1c087ffdc059
Cipher  1 :  e6de5688e74b7ef31dbe6942d156ed0a
Cipher  2 :  e6de56abe74b4ff31d7669426556ed0a

Xor Variation

Message                 :  0000000000000000007c000000000000
Round Key Apply         :  0000000000000000007c000000000000
First Round Sub         :  0000000000000000003f000000000000
First Round Shift       :  00000000000000000000003f00000000
First Round Mix Col     :  0000003f000000410000007e0000003f
First Round Key Apply   :  0000003f000000410000007e0000003f
Second Round Sub        :  0000002300000031000000c8000000b4
Second Round Shift      :  000000230000310000c80000b4000000
Second Round Key Apply  :  000000230000310000c80000b4000000
CipherText              :  000000230000310000c80000b4000000

Cipher Diff
[(3, '88', 'ab'), (6, '7e', '4f'), (9, 'be', '76'), (12, 'd1', '65')]

============================================================

location 2,2

Message 1 :  c8770072bb859a5bf53b8c8f5d040b75
Message 2 :  c8770072bb859a5bf53bff8f5d040b75
Cipher  1 :  c3e83b4ef47954c48542119218855d91
Cipher  2 :  fae83b4ef47954078542fa9218a55d91

Xor Variation

Message                 :  00000000000000000000730000000000
Round Key Apply         :  00000000000000000000730000000000
First Round Sub         :  00000000000000000000720000000000
First Round Shift       :  00000000000000007200000000000000
First Round Mix Col     :  7200000096000000e400000072000000
First Round Key Apply   :  7200000096000000e400000072000000
Second Round Sub        :  39000000c3000000eb00000020000000
Second Round Shift      :  39000000000000c30000eb0000200000
Second Round Key Apply  :  39000000000000c30000eb0000200000
CipherText              :  39000000000000c30000eb0000200000

Cipher Diff
[(0, 'c3', 'fa'), (7, 'c4', '07'), (10, '11', 'fa'), (13, '85', 'a5')]

============================================================

location 2,3

Message 1 :  14052d9ef4135d5d149aec8cec8bdc10
Message 2 :  14052d9ef4135d5d149aecffec8bdc10
Cipher  1 :  7a9eac76eb74723d5b52eeb401166125
Cipher  2 :  7a31ac761874723d5b52ee1f01167425

Xor Variation

Message                 :  00000000000000000000007300000000
Round Key Apply         :  00000000000000000000007300000000
First Round Sub         :  00000000000000000000002600000000
First Round Shift       :  00000000000000000026000000000000
First Round Mix Col     :  00260000006a0000004c000000260000
First Round Key Apply   :  00260000006a0000004c000000260000
Second Round Sub        :  00af000000f3000000ab000000150000
Second Round Shift      :  00af0000f3000000000000ab00001500
Second Round Key Apply  :  00af0000f3000000000000ab00001500
CipherText              :  00af0000f3000000000000ab00001500

Cipher Diff
[(1, '9e', '31'), (4, 'eb', '18'), (11, 'b4', '1f'), (14, '61', '74')]

============================================================

location 3,0

Message 1 :  26663b79b3f7c76b275efee17c2d3352
Message 2 :  26663b79b3f7c76b275efee1ff2d3352
Cipher  1 :  9ba733799a383dc2921a63054aac9991
Cipher  2 :  9b8f3379e0383dc2921a63ab4aac1991

Xor Variation

Message                 :  00000000000000000000000083000000
Round Key Apply         :  00000000000000000000000083000000
First Round Sub         :  0000000000000000000000001e000000
First Round Shift       :  000000000000000000000000001e0000
First Round Mix Col     :  001e0000001e000000220000003c0000
First Round Key Apply   :  001e0000001e000000220000003c0000
Second Round Sub        :  00280000007a000000ae000000800000
Second Round Shift      :  002800007a000000000000ae00008000
Second Round Key Apply  :  002800007a000000000000ae00008000
CipherText              :  002800007a000000000000ae00008000

Cipher Diff
[(1, 'a7', '8f'), (4, '9a', 'e0'), (11, '05', 'ab'), (14, '99', '19')]

============================================================

location 3,1

Message 1 :  9ef887a5805d1ef156b3b14d934bf06c
Message 2 :  9ef887a5805d1ef156b3b14d93fff06c
Cipher  1 :  709083c1de6f61378705d78707121a02
Cipher  2 :  70904fc1de076137fb05d78707121a23

Xor Variation

Message                 :  00000000000000000000000000b40000
Round Key Apply         :  00000000000000000000000000b40000
First Round Sub         :  00000000000000000000000000f80000
First Round Shift       :  0000000000000000000000000000f800
First Round Mix Col     :  0000f8000000f800000013000000eb00
First Round Key Apply   :  0000f8000000f800000013000000eb00
Second Round Sub        :  0000cc000000680000007c0000002100
Second Round Shift      :  0000cc00006800007c00000000000021
Second Round Key Apply  :  0000cc00006800007c00000000000021
CipherText              :  0000cc00006800007c00000000000021

Cipher Diff
[(2, '83', '4f'), (5, '6f', '07'), (8, '87', 'fb'), (15, '02', '23')]

============================================================

location 3,2

Message 1 :  bd7237dbd1b60179a953285ae0dff0f6
Message 2 :  bd7237dbd1b60179a953285ae0dffff6
Cipher  1 :  5404be8abf23526238391e26a7c335c1
Cipher  2 :  5404bed6bf23316238781e2680c335c1

Xor Variation

Message                 :  00000000000000000000000000000f00
Round Key Apply         :  00000000000000000000000000000f00
First Round Sub         :  00000000000000000000000000008500
First Round Shift       :  00000000000000000000000000000085
First Round Mix Col     :  00000085000000850000009400000011
First Round Key Apply   :  00000085000000850000009400000011
Second Round Sub        :  0000005c000000630000004100000027
Second Round Shift      :  0000005c000063000041000027000000
Second Round Key Apply  :  0000005c000063000041000027000000
CipherText              :  0000005c000063000041000027000000

Cipher Diff
[(3, '8a', 'd6'), (6, '52', '31'), (9, '39', '78'), (12, 'a7', '80')]

============================================================

location 3,3

Message 1 :  59d0b9515b009b6c69aa9654339a2d8b
Message 2 :  59d0b9515b009b6c69aa9654339a2dff
Cipher  1 :  992b44622099b43ee6539288017123b6
Cipher  2 :  c32b44622099b409e653e788012223b6

Xor Variation

Message                 :  00000000000000000000000000000074
Round Key Apply         :  00000000000000000000000000000074
First Round Sub         :  000000000000000000000000000000b9
First Round Shift       :  000000000000000000000000b9000000
First Round Mix Col     :  b9000000b9000000d000000069000000
First Round Key Apply   :  b9000000b9000000d000000069000000
Second Round Sub        :  5a000000370000007500000053000000
Second Round Shift      :  5a000000000000370000750000530000
Second Round Key Apply  :  5a000000000000370000750000530000
CipherText              :  5a000000000000370000750000530000

Cipher Diff
[(0, '99', 'c3'), (7, '3e', '09'), (10, '92', 'e7'), (13, '71', '22')]

============================================================
```
