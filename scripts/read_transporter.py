# Go to root of PyNTRReader
import sys
sys.path.append('../')

from structure import PK6
from ntrreader import G6Reader
from ip import IP_ADDR

client = G6Reader(IP_ADDR)

print(PK6(client.readTransporter()))