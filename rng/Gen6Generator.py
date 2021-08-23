from rng import Generator, Frame, MT, RNGList
from pokeconstants import *

class Gen6Generator(Generator):
    
    def __init__(self,seed,tsv,charm,method,delay,sync,ivs,shiny,ability,gender):
        rng = MT(seed)
        pool = RNGList(rng,128)
        super().__init__(rng, pool)
        self.method = method
        self.delay = delay
        self.tsv = tsv
        self.sync = sync
        self.ivs = ivs
        self.shiny = shiny
        self.ability = ability
        self.gender = gender
        if self.shiny != SHINY_LOCKED and self.sync != ALWAYS_SYNC and charm:
            self.rerolls = 3
        else:
            self.rerolls = 1
        self.frame = -1
        self.advance(delay+1,False)
    def generate(self):
        if self.sync == CAN_SYNC or self.method > STATIONARY:
            self.pool.advanceFrames(60)
        if self.method == HORDE:
            result = []
            for slot in range(5):
                result.append(Frame(self.method,[self.frame, slot + 1] + self.generate_once()))
        else:
            result = Frame(self.method,[self.frame] + self.generate_once())
        self.skip()
        return result
    def generate_once(self):
        shiny = NON_SHINY
        EC = self.pool.getValue()
        for i in range(self.rerolls):
            PID = self.pool.getValue()
            PSV = ((PID >> 16) ^ (PID & 0xFFFF))
            XOR = self.tsv ^ PSV
            if XOR < 8:
                if self.shiny == SHINY_LOCKED:
                    PID ^= 0x10000000
                    PSV = ((PID >> 16) ^ (PID & 0xFFFF))
                    shiny = NON_SHINY
                else:
                    shiny = STAR
                    if XOR == 0:
                        shiny = SQUARE
                break
            elif self.shiny == FORCED_SHINY:
                PID = (((((self.tsv << 4) + self.trv) ^ (PID & 0xFFFF)) << 16) + (PID & 0xFFFF)) & 0xFFFFFFFF
                PSV = ((PID >> 16) ^ (PID & 0xFFFF))
                shiny = SQUARE
        
        IVs = [-1]*6
        i = self.ivs
        while i > 0:
            tmp = self.pool.rand(6)
            if IVs[tmp] < 0:
                i -= 1
                IVs[tmp] = 31
        for i in range(6):
            if IVs[i] < 0:
                IVs[i] = self.pool.getValue() >> 27
        
        if self.ability == ABILITY_12:
            ability = (self.pool.getValue() >> 31) + 1
        elif self.ability == ABILITY_12H:
            ability = self.pool.rand(3) + 1
        else:
            ability = self.ability
        
        if self.sync == ALWAYS_SYNC:
            nature = 25
        else:
            nature = self.pool.rand(25)
        
        if self.gender == GENDER_MF:
            gender = self.pool.rand(252)
        else:
            gender = self.gender
        return [EC, PID, PSV, shiny, IVs, ability, nature, gender]
    def skip(self,add_frame=True):
        self.pool.advanceState()
        if add_frame:
            self.frame += 1
    def advance(self,advances,add_frame=True):
        for _ in range(advances):
            self.skip(add_frame=True)