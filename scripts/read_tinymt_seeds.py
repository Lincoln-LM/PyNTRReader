# Script to read TinyMT Seeds from 3ds memory
import sys
sys.path.append('../')

from time import sleep
from ntrreader import G6Reader
from rng import TinyMT
from ip import IP_ADDR

reader = G6Reader(IP_ADDR)

last_tiny_seeds = []

tiny_seeds = []
initial_seeds = []
ind = 0
for index in range(3,-1,-1):
    initial_seeds.append(reader.readU32(reader.tinyStart+(index*4)))
go = TinyMT(state=initial_seeds)
while True:
    for index in range(3,-1,-1):
        tiny_seeds.append(reader.readU32(reader.tinyStart+(index*4)))
    if tiny_seeds != last_tiny_seeds:
        b = False
        pre = ind
        prestate = go.state.copy()
        rev = go.state.copy()
        rev.reverse()
        add = 0
        while str(rev) != str(tiny_seeds):
            go.next()
            rev = go.state.copy()
            rev.reverse()
            add += 1
            if add > 10000:
                add = 0
                go.state = prestate
                b = True
                break
        ind += add
        if not b:
            print(f"Index: {ind}")
            print("Current Seeds:")
            print(go.display_state())
        last_tiny_seeds = tiny_seeds
    tiny_seeds = []

    sleep(1/60)