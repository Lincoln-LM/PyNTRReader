import socket
from enum import Enum
from array import array
from time import sleep
import re
from ntrreader import LumaInputServer


class PyNTRReader:
    def __init__(self, host, input=False, debug=False):
        self.input = input
        self.debug = debug
        self.sequence = 0
        self.host = host
        self.pid = -1
        self.game_name = None
        self.start_connection()
        self.XY = False
        self.ORAS = False
        self.Transporter = False
        self.Gold = False
        self.game = -1  # 0:XY 1:ORAS
        self.title = ""
        self.titles = ["kujira-1", "kujira-2", "sango-1", "sango-2",
                       "salmon", "niji_loc", "niji_loc", "momiji", "momiji", "trl"]
        for title in self.titles:
            self.set_game_name(title)
            if self.pid != -1:
                self.title = title
                if self.title in ["kujira-1", "kujira-2"]:
                    self.XY = True
                elif self.title == "salmon":
                    self.Transporter = True
                elif self.title == "trl":
                    self.Gold = True
                else:
                    self.ORAS = True
                break
        if self.debug:
            self.socket = socket.create_connection((self.host, 5000+self.pid))
            self.send_heartbeat_packet()
            self.bpdis(3)
            self.bpdis(4)
            self.resume()
            self.bpena(3)

    def set_game_name(self, name):
        self.game_name = name
        self.send_processes_packet()
        self.send_heartbeat_packet()
        self.read_packet()
        return self.pid

    def read_packet(self):
        packet_header = self.socket.recv(84)
        if len(packet_header) == 0:
            return None

        while len(packet_header) < 84:
            packet_header += self.socket.recv(84 - len(packet_header))

        packet_header = array('I', packet_header)
        packet_data = b''
        while len(packet_data) < packet_header[20]:
            packet_data += self.socket.recv(
                packet_header[20] - len(packet_data))

        if packet_header[3] == 0:
            if self.game_name is not None:
                m = re.search(
                    'pid: 0x([0-9a-f]{8}), pname:\s+%s' % self.game_name, packet_data.decode())
                if m:
                    self.pid = int(m.group(1), 16)
                    # print("Setting pid to %x" % self.pid)

            return 0
        elif packet_header[3] == 9:
            return packet_data
        else:
            return 0xDEADC0DE

    def send_packet(self, packet_type, command, args=[], data=b''):
        self.sequence += 1000
        packet_header = array(
            'I', (0x12345678, self.sequence, packet_type, command))
        packet_header.extend(args)
        packet_header.extend([0] * (16 - len(args)))
        packet_header.append(len(data))  # len(data)
        self.socket.sendall(packet_header.tobytes() + data)

    def start_connection(self):
        if self.input:
            self.input_socket = LumaInputServer(self.host)
        self.socket = socket.create_connection((self.host, 8000))
        self.send_heartbeat_packet()
        packet = self.read_packet()
        

    # Sending packets

    def send_heartbeat_packet(self):
        # print("Sending Heartbeat Packet")
        self.send_packet(0, 0)

    def send_hello_packet(self):
        # print("Sending Hello Packet")
        self.send_packet(0, 3)

    def send_reload_packet(self):
        # print("Sending Reload Packet")
        self.send_packet(0, 4)

    def send_processes_packet(self):
        # print("Sending Processes Packet")
        self.send_packet(0, 5)

    def send_addresses_packet(self):
        # print("Sending Addresses Packet")
        self.send_packet(0, 8)

    def send_read_memory_packet(self, addr, length):
        # print("Sending RMemory Packet")
        # print("%02x\t%08x\t%x" % (self.pid, addr, length))
        self.send_packet(0, 9, [self.pid, addr, length])
    
    def bpdis(self,id):
        self.send_packet(0,11,[id,0,3])

    def bpena(self,id):
        self.send_packet(0,11,[id,0,2])

    def bpadd(self,addr):
        self.send_packet(0,11,[1,addr,1])

    def resume(self):
        self.send_packet(0,11,[0,0,4])

    def send_write_memory_packet(self, addr, length, data):
        # print("Sending WMemory Packet")
        # print("%02x\t%08x\t%x" % (self.pid, addr, length))
        #print("Data: "+data)
        self.send_packet(0, 10, [self.pid, addr, length], data)

    # Improved UI Commands

    # Writing

    def write(self, addr, data, length, isSigned=False):
        # Safety checks and stuff
        t = type(data)
        if t == type(0):
            if ((data >= 0x00) and (data < (0x100 ** length))):
                data = data.to_bytes(length, 'little', signed=isSigned)
            else:
                raise Exception(
                    "WriteU%i: Invalid Data, must be in range 0-%i" % (8*length, ((0x100 * length)-1)))
        self.send_write_memory_packet(addr, length, data)

    def writeU8(self, addr, data):
        self.write(addr, data, 1)

    def writeU16(self, addr, data):
        self.write(addr, data, 2)

    def writeU32(self, addr, data):
        self.write(addr, data, 4)

    def writeU64(self, addr, data):
        self.write(addr, data, 8)

    def write8(self, addr, data):
        self.write(addr, data, 1, isSigned=True)

    def write16(self, addr, data):
        self.write(addr, data, 2, isSigned=True)

    def write32(self, addr, data):
        self.write(addr, data, 4, isSigned=True)

    def write64(self, addr, data):
        self.write(addr, data, 8, isSigned=True)

    # Reading

    def read(self, addr, length):
        self.send_read_memory_packet(addr, length)
        return self.read_packet()

    def readU8(self, addr):
        return int.from_bytes(self.read(addr, 1), byteorder='little', signed=False)

    def readU16(self, addr):
        return int.from_bytes(self.read(addr, 2), byteorder='little', signed=False)

    def readU32(self, addr):
        return int.from_bytes(self.read(addr, 4), byteorder='little', signed=False)

    def readU64(self, addr):
        return int.from_bytes(self.read(addr, 8), byteorder='little', signed=False)

    def readU8(self, addr):
        return int.from_bytes(self.read(addr, 1), byteorder='little', signed=False)

    def readU16(self, addr):
        return int.from_bytes(self.read(addr, 2), byteorder='little', signed=False)

    def readU32(self, addr):
        return int.from_bytes(self.read(addr, 4), byteorder='little', signed=False)

    def readU64(self, addr):
        return int.from_bytes(self.read(addr, 8), byteorder='little', signed=False)

class G2Reader(PyNTRReader):
    PK6STOREDSIZE = 0xE8
    PK6PARTYSIZE = 0x104

    def __init__(self, ip, input=False, debug=False):
        PyNTRReader.__init__(self, ip, input=input, debug=debug)
        self.baseAddress = 0x8A2406C
    
    def readGB(self,address,length):
        return self.read(self.baseAddress + address, length)

    def readWild(self):
        return self.readGB(0xCC13,0x4FF)
        

class G6Reader(PyNTRReader):
    PK6STOREDSIZE = 0xE8
    PK6PARTYSIZE = 0x104

    def __init__(self, ip, input=False, debug=False):
        PyNTRReader.__init__(self, ip, input=input, debug=debug)
        if self.XY:
            self.partyAddress = 0x8CE1CF8

            self.initialSeed = None
            self.seedAddress = 0x8c52844
            self.idAddress = 0x8c79c3c
            self.mtStart = 0x8c5284C
            self.mtIndex = 0x8c52848

            self.tinyStart = 0x8c52808

            self.eggReady = 0x8C80124
            self.eggAddress = 0x8c8012c
            self.parent1Address = 0x8C7FF4C
            self.parent2Address = 0x8C8003C

            self.saveVariable = 0x8C6A6A4
        elif self.ORAS:
            self.partyAddress = 0x8CFB26C

            self.initialSeed = None
            self.seedAddress = 0x8c59e40
            self.idAddress = 0x8c81340
            self.mtStart = 0x8c59e48
            self.mtIndex = 0x8c59e44

            self.tinyStart = 0x8C59E04

            self.eggReady = 0x8C88358
            self.eggAddress = 0x8C88360
            self.eggReady2 = 0x8C88548
            self.eggAddress2 = 0x8C88550
            self.parent1Address = 0x8C88180
            self.parent2Address = 0x8C88270

            self.saveVariable = 0x8C71DB8
        elif self.Transporter:
            self.transporterAddress = 0x8BC6524
        self.IDs = self.readIDs()
        self.TSV = self.IDs[0] ^ self.IDs[1]
        print(f"Game: {'XY' if self.XY else 'ORAS'} TID: {self.IDs[0]} TSV: {self.TSV >> 4} TRV: {self.TSV%16} FULL TSV: {self.TSV}\n")
    
    def readIDs(self):
        ids = self.readU32(self.idAddress)
        return ids >> 16, ids & 0xFFFF

    def getWildOffset(self):
        if self.game == 0:
            pointer = self.readU32(0x880313c) - 0xA1C
            if pointer < 0x8000000 or pointer > 0x8DF0000:
                return 0x8805614
            else:
                pointer = self.readU32(pointer)
                if pointer < 0x8000000 or pointer > 0x8DF0000:
                    return 0x8805614
                else:
                    return pointer
        else:
            pointer = self.readU32(0x880313c) - 0x22C0
            if pointer < 0x8000000 or pointer > 0x8DF0000:
                return 0x8804064 if self.readU32(0x8804060) == 0 else 0x8804060
            else:
                pointer = self.readU32(pointer)
                if pointer < 0x8000000 or pointer > 0x8DF0000:
                    return 0x8804064 if self.readU32(0x8804060) == 0 else 0x8804060
                else:
                    return pointer

    def readWild(self):
        return self.read(self.getWildOffset(), self.PK6PARTYSIZE)

    def readRadar(self):
        return self.read(self.getWildOffset() - 0x198, self.PK6PARTYSIZE)
    
    def readFish(self):
        return self.read(self.getWildOffset() + 0xaa8, self.PK6PARTYSIZE)

    def readHordeSlot(self, slot):
        return self.read(self.getWildOffset() + (slot * 0x1e4), self.PK6PARTYSIZE)
    
    def readHorde(self):
        return [self.readHordeSlot(0), self.readHordeSlot(1), self.readHordeSlot(2), self.readHordeSlot(3), self.readHordeSlot(4)]

    def readEgg(self, daycare=0):
        if daycare == 1 and self.game == 1:
            ready = self.readU32(self.eggReady2)

            seed0 = self.readU32(self.eggAddress2)
            seed1 = self.readU32(self.eggAddress2 + 4)

            return ready, seed1, seed0
        ready = self.readU32(self.eggReady)

        seed0 = self.readU32(self.eggAddress)
        seed1 = self.readU32(self.eggAddress + 4)

        return ready, seed1, seed0
    
    def readTransporter(self):
        return self.read(self.transporterAddress, self.PK6PARTYSIZE)
