from time import time
from Listing7_1 import compare_mac
from Listing7_3 import cmp_const

MAC1 = '0123456789abcdef'
MAC2 = '01X3456789abcdef'
TRIALS = 100000


print('With Listing 7-1')
start = time()
for i in range(TRIALS):
    compare_mac(MAC1, MAC1, len(MAC1))
    # cmp_const(MAC1, MAC1, len(MAC1))
end = time()
print('%0.5f' % (end-start))

start = time()
for i in range(TRIALS):
    compare_mac(MAC1, MAC2, len(MAC1))
    # cmp_const(MAC1, MAC1, len(MAC1))
end = time()
print('%0.5f' % (end-start))
