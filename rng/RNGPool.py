class RNGList:
    def __init__(self,rng,size):
        self.states = []
        self.head = 0
        self.pointer = 0
        self.rng = rng
        self.size = size
        for i in range(self.size):
            self.states.append(self.rng.next())
    
    def advanceFrames(self,advances):
        for _ in range(advances):
            self.advanceFrame()

    def advanceFrame(self):
        self.head &= self.size - 1
        self.states[self.head] = self.rng.next()
        self.head += 1
        self.pointer = self.head
    
    def advanceInFrame(self,advances):
        self.pointer = (self.pointer + advances) & (self.size - 1)
    
    def getValue(self):
        self.pointer &= self.size - 1
        self.pointer += 1
        return self.states[self.pointer-1]
    
    def resetState(self):
        self.pointer = self.head
    
    def rand(self,n):
        return ((self.getValue() * n) >> 32) & 0xFFFFFFFF

    def randBool(self):
        return self.getValue() < 0x80000000
