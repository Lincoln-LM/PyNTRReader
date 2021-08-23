from rng import Generator, MT, RNGList

class StationaryGenerator(Generator):
    NATURES = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty",
               "Bold", "Docile", "Relaxed", "Impish", "Lax",
               "Timid", "Hasty", "Serious", "Jolly", "Naive",
               "Modest", "Mild", "Quiet", "Bashful", "Rash",
               "Calm", "Gentle", "Sassy", "Careful", "Quirky" 
                              "Synchronize"]
    CAN_SYNC = 0
    CAN_NOT_SYNC = 1
    ALWAYS_SYNC = 2

    CAN_BE_SHINY = 0
    SHINY_LOCKED = 1
    FORCED_SHINY = 2

    ABILITY_NA = 0
    ABILITY_1 = 1
    ABILITY_2 = 2
    ABILITY_HA = 3

    GENDER_NA = 0
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_NONE = 3

    NON_SHINY = 0
    STAR = 1
    SQUARE = 2
    def __init__(self,seed,tsv,charm,sync,ivs,shiny,ability, gender):
        rng = MT(seed)
        pool = RNGList(rng,128)
        super().__init__(rng, pool)
        self.tsv = tsv
        self.sync = sync
        self.ivs = ivs
        self.shiny = shiny
        self.ability = ability
        self.gender = gender
        if self.shiny != self.SHINY_LOCKED and self.sync != self.ALWAYS_SYNC and charm:
            self.rerolls = 3
        else:
            self.rerolls = 1
        self.pool.advanceState()
        self.frame = -1
    def generate(self):
        if self.sync != self.ALWAYS_SYNC:
            self.pool.advanceFrames(60)
        shiny = self.NON_SHINY
        EC = self.pool.getValue()
        for i in range(self.rerolls):
            PID = self.pool.getValue()
            PSV = ((PID >> 16) ^ (PID & 0xFFFF))
            XOR = self.tsv ^ PSV
            if XOR < 8:
                if self.shiny == self.SHINY_LOCKED:
                    PID ^= 0x10000000
                    PSV = ((PID >> 16) ^ (PID & 0xFFFF))
                    shiny = self.NON_SHINY
                else:
                    shiny = self.STAR
                    if XOR == 0:
                        shiny = self.SQUARE
                break
            elif self.shiny == self.FORCED_SHINY:
                PID = (((((self.tsv << 4) + self.trv) ^ (PID & 0xFFFF)) << 16) + (PID & 0xFFFF)) & 0xFFFFFFFF
                PSV = ((PID >> 16) ^ (PID & 0xFFFF))
                shiny = self.SQUARE
        
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
        
        if self.ability == self.ABILITY_NA:
            ability = (self.pool.getValue() >> 31) + 1
        else:
            ability = self.ability
        
        if self.sync == self.ALWAYS_SYNC:
            nature = 25
        else:
            nature = self.pool.rand(25)
        
        if self.gender == self.GENDER_NA:
            gender = self.pool.rand(252)
        else:
            gender = self.gender
        self.pool.advanceState()
        self.frame += 1
        return [self.frame, EC, PID, PSV, shiny, IVs, ability, nature, gender]
    def skip(self):
        self.pool.advanceState()
        self.frame += 1
    def advance(self,advances):
        for _ in range(advances):
            self.skip()
    def header(self):
        return "Frame EC PID PSV Shiny IVs Ability Nature Gender"
    def format(self,frame):
        return f"{frame[0]} {frame[1]:08X} {frame[2]:08X} {frame[3]:05d} {'Square' if frame[4] == self.SQUARE else 'Star' if frame[4] == self.STAR else 'Not Shiny'} {'/'.join(str(iv) for iv in frame[5])}, {frame[6]}, {self.NATURES[frame[7]]}, {frame[8]}"

        


