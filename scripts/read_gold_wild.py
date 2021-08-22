# Go to root of PyNTRReader
import sys
sys.path.append('../')

from ntrreader import G2Reader
from structure import PK2
from ip import IP_ADDR

client = G2Reader(IP_ADDR,input=True)
oldinfo = ""
while True:
    pk2 = PK2.battle(client.readWild())
    info = str(pk2)
    if info != oldinfo and pk2.isValid:
        print(info)
        oldinfo = info
    