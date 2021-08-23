from pokeconstants import *

class Generator:
    def __init__(self, rng, pool):
        self.rng = rng
        self.pool = pool

class Frame:
    NATURES = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty",
               "Bold", "Docile", "Relaxed", "Impish", "Lax",
               "Timid", "Hasty", "Serious", "Jolly", "Naive",
               "Modest", "Mild", "Quiet", "Bashful", "Rash",
               "Calm", "Gentle", "Sassy", "Careful", "Quirky",
                              "Synchronize"]
    def __init__(self, method, frame_list):
        self.method = method
        horde = 1 if self.method == HORDE else 0
        self.Frame = frame_list[0]
        self.Slot = frame_list[1]
        self.EC = frame_list[1+horde]
        self.PID = frame_list[2+horde]
        self.PSV = frame_list[3+horde]
        self.Shiny = frame_list[4+horde]
        self.IVs = frame_list[5+horde]
        self.Ability = frame_list[6+horde]
        self.Nature = frame_list[7+horde]
        self.Gender = frame_list[8+horde]
        
        self.Perfect_IV_Count = self.IVs.count(31)
    def header(self):
        return f"Frame {'Slot ' if self.method == HORDE else ''}EC PID PSV Shiny IVs Ability Nature Gender"
    def __str__(self):
        return f"{self.Frame} {str(self.Slot)+' ' if self.method == HORDE else ''}{self.EC:08X} {self.PID:08X} {self.PSV:05d} {'Square' if self.Shiny == SQUARE else 'Star' if self.Shiny == STAR else 'Not Shiny'} {'/'.join(str(iv) for iv in self.IVs)}, {'H' if self.Ability > 2 else self.Ability}, {self.NATURES[self.Nature]}, {self.Gender}"

