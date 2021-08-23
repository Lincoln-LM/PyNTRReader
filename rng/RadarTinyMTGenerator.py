from rng import Generator, TinyMT, RNGList

class RadarTinyMTGenerator(Generator):

    PATCHES = [
    ["#","#","#","#","#","#","#","#","#"],
    ["#","#","#","#","#","#","#","#","#"],
    ["#","#","#","#","#","#","#","#","#"],
    ["#","#","#","#","#","#","#","#","#"],
    ["#","#","#","#","C","#","#","#","#"],
    ["#","#","#","#","#","#","#","#","#"],
    ["#","#","#","#","#","#","#","#","#"],
    ["#","#","#","#","#","#","#","#","#"],
    ["#","#","#","#","#","#","#","#","#"]
          ]
    GOOD_RATE = [23,43,63,83]

    def __init__(self,state,party_count,chain_count,boost,search_for_shiny):
        self.state_count = TinyMT(state=state.copy())
        rng = TinyMT(state=state.copy())
        pool = RNGList(rng,128)
        super().__init__(rng, pool)
        self.index = 0
        self.party_count = party_count
        self.chain_count = chain_count
        self.boost = boost
        self.search_for_shiny = search_for_shiny
    def generate(self):
        status = self.state_count.display_state()
        self.pool.advanceInFrame(3*self.party_count)
        music_val = self.pool.rand(100)
        boost = self.boost
        boost &= 1 if music_val >= 50 else 0
        has_shiny = False
        if not self.search_for_shiny:
            patches = self.PATCHES.copy()
            ring = 0
            while ring < 4:
                state = "B"
                direction = self.pool.rand(4)
                location = self.pool.rand(ring * 2 + 3)
                if self.pool.rand(100) < self.GOOD_RATE[ring]:
                    state = "G"
                    self.pool.getValue()
                    chance = 100 if boost or self.chain_count >= 40 else (8100 - self.chain_count * 200)
                    if self.pool.getValue() * chance <= 0xFFFFFFFF:
                        has_shiny = True
                        state = "S" 
                self.set_patch(patches, ring, direction, location, state)
                ring += 1
            ring = self.pool.rand(3)
            direction = self.pool.rand(4)
            location = self.pool.rand(ring * 2 + 3)
            state = "X"
            self.set_patch(patches, ring, direction, location, state)
            result = [self.index, status, patches, has_shiny]
        else:
            for i in range(4):
                self.pool.getValue()
                self.pool.getValue()
                if self.pool.rand(100) < self.GOOD_RATE[i]:
                    self.pool.getValue()
                    chance = 100 if boost or self.chain_count >= 40 else (8100 - self.chain_count * 200)
                    if self.pool.getValue() * chance <= 0xFFFFFFFF:
                        has_shiny = True
            result = [self.index, status, has_shiny]
        self.skip()
        return result
    @staticmethod
    def set_patch(patches, ring, direction, location, state):
        if direction == 0 or direction == 1:
            x = 3 - ring + location
        elif direction == 2:
            x = 3 - ring
        elif direction == 3:
            x = 5 + ring
        else:
            x = 4
        if direction == 0:
            y = 3 - ring
        elif direction == 1:
            y = 5 + ring
        elif direction == 2 or direction == 3:
            y = 3 - ring + location
        else:
            y = 4
        patches[y][x] = state
    @staticmethod
    def display_patches(patches):
        return "\n".join(" ".join(patches[x]) for x in range(9))
    def skip(self):
        self.pool.advanceFrame()
        self.state_count.next()
        self.index += 1
    def advance(self,advances):
        for _ in range(advances):
            self.skip()
    