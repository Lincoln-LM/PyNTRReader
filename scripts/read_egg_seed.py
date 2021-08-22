# Go to root of PyNTRReader
import sys
sys.path.append('../')

from ntrreader import G6Reader
from ip import IP_ADDR

client = G6Reader(IP_ADDR)

ready, seed1, seed0 = client.readEgg(1)
print(hex(seed1),hex(seed0))