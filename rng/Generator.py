from os import stat


class Generator:
    def __init__(self, rng, pool):
        self.rng = rng
        self.pool = pool
    def format(self, frame):
        pass
    def generate(self):
        pass

class Frame:
    NATURES = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty",
               "Bold", "Docile", "Relaxed", "Impish", "Lax",
               "Timid", "Hasty", "Serious", "Jolly", "Naive",
               "Modest", "Mild", "Quiet", "Bashful", "Rash",
               "Calm", "Gentle", "Sassy", "Careful", "Quirky",
                              "Synchronize"]
    def __init__(self, frame_list):
        self.Frame = frame_list[0]
        self.EC = frame_list[1]
        self.PID = frame_list[2]
        self.PSV = frame_list[3]
        self.Shiny = frame_list[4]
        self.IVs = frame_list[5]
        self.Ability = frame_list[6]
        self.Nature = frame_list[7]
        self.Gender = frame_list[8]
        
        self.Perfect_IV_Count = self.IVs.count(31)
    @staticmethod
    def header():
        return "Frame EC PID PSV Shiny IVs Ability Nature Gender"
    def __str__(self):
        return f"{self.Frame} {self.EC:08X} {self.PID:08X} {self.PSV:05d} {'Square' if self.Shiny == 2 else 'Star' if self.Shiny == 1 else 'Not Shiny'} {'/'.join(str(iv) for iv in self.IVs)}, {self.Ability}, {self.NATURES[self.Nature]}, {self.Gender}"

