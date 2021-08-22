from structure.ByteStruct import ByteStruct

class PK2(ByteStruct):
    STOREDSIZE = 32
    PARTYSIZE = 48

    def __init__(self,buf):
        self.data = bytearray(buf[:])
    
    @staticmethod
    def battle(buf):
        pk2 = PK2(([0]*32)[:])
        # Moves
        pk2.data[2] = buf[0] 
        pk2.data[3] = buf[1]
        pk2.data[4] = buf[2]
        pk2.data[5] = buf[3]
        # DVs
        pk2.setushort(0x15,int.from_bytes(buf[0x4E2:0x4E2 + 2], byteorder='big'))
        # Species
        pk2.data[0] = buf[0x4DA]
        return pk2

    @property
    def species(self):
        return self.getbyte(0x0)

    @property
    def helditem(self):
        return self.getbyte(0x1)

    @property
    def tid(self):
        return self.getushort(0x6)

    @property
    def move1(self):
        return self.getbyte(0x2)

    @property
    def move2(self):
        return self.getbyte(0x3)

    @property
    def move3(self):
        return self.getbyte(0x4)

    @property
    def move4(self):
        return self.getbyte(0x5)

    @property
    def dv16(self):
        return self.getushort(0x15)

    @property
    def dvs(self):
        dv16 = self.dv16
        atk = dv16 >> 12
        defe = (dv16 >> 8) & 0xF
        spe = (dv16 >> 4) & 0xF
        spc = dv16 & 0xF
        hp = ((atk & 0x1) << 3) + ((defe & 0x1) << 2) + ((spe & 0x1) << 1) + (spc & 0x1)
        return [hp, atk, defe, spe, spc]

    @property
    def shinyType(self):
        return (self.dv16 & 0xFF2F) == 0xAA2A

    @property
    def shinyString(self):
        return 'None' if not self.shinyType else 'Shiny'
    
    @property
    def isValid(self):
        return not (self.move1 == 0)

    def save(self,filename):
        with open(f'{filename}.PK2','wb') as fileOut:
            fileOut.write(self.data)

    def __str__(self):
        from lookups import Util
        msg = f"{Util.STRINGS.species[self.species]}{' ' if not self.shinyType else ' ⋆'}\n"
        msg += f"DVs: {self.dvs}\n"
        msg += f"Moves: {Util.STRINGS.moves[self.move1]} / {Util.STRINGS.moves[self.move2]} / {Util.STRINGS.moves[self.move3]} / {Util.STRINGS.moves[self.move4]}\n"
        return msg
