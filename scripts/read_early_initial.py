# Go to root of PyNTRReader
import sys
sys.path.append('../')

from ntrreader import G6Reader
from ip import IP_ADDR

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
    index = client.readU32(client.mtIndex)A
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
    # Update last_index
    last_index = index