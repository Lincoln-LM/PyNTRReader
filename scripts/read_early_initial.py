# Go to root of PyNTRReader
import sys
sys.path.append('../')

from ntrreader import G6Reader
from ip import IP_ADDR
from rng import Gen6Generator
from pokeconstants import *

# Function to reverse the initialization of the MT array (before shuffling/tempering)
def reverse_init(s, i):
    s = (0x9638806D * (s - i)) & 0xffffffff
    return s ^ s >> 30

# Connect to 3ds
client = G6Reader(IP_ADDR)
# Set last_index to 624 so it always starts above index
last_index = 624
while True:
    # Read the current MT index
    index = client.readU32(client.mtIndex)
    # Check if the current index is less than the last index 
    # If it is then the script is either just starting, the index passed 624, or a new initial seed has been generated
    if index < last_index:
        # Read the last number in the MT's initial array and store to initial_seed (this is not the initial seed)
        initial_seed = client.readU32(client.mtIndex+624*4)
        # Reverse the initialization to get the actual initial seed
        for i in range(623, 0, -1):
            initial_seed = reverse_init(initial_seed, i)
        # Print the initial seed
        print(f"Initial Seed: {initial_seed:08X}\n")
        # Example for checking if a seed is what you want
        # Set up chain 0 pokeradar generator
        gen = Gen6Generator(initial_seed,client.TSV,False,POKE_RADAR,14,CAN_SYNC,0,CAN_BE_SHINY,ABILITY_12,GENDER_MF)
        header_printed = False
        # Check the first 100000 frames
        for _ in range(100000):
            frame = gen.generate()
            if not header_printed:
                print(frame.header())
                header_printed = True
            # Example Filter for the frames, checks if its at least 3ivs and shiny
            if frame.Perfect_IV_Count >= 3 and frame.Shiny:
                print(frame)
    # Update last_index
    last_index = index