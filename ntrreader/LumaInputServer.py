import builtins
import socket
from time import sleep
class LumaInputServer():
    def __init__(self, server, port=4950):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = 4950
        self.socket.connect((server, port))
        self.empty = [0xFF, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x08, 0x80, 0x00]
        self.buttons = {
                        "NONE":  0xFF,
                        "A":     0xFF^(1<<0),
                        "B":     0xFF^(1<<1),
                        "SELECT":0xFF^(1<<2),
                        "START": 0xFF^(1<<3),
                        "RIGHT": 0xFF^(1<<4),
                        "LEFT":  0xFF^(1<<5),
                        "UP":    0xFF^(1<<6),
                        "DOWN":  0xFF^(1<<7),
                        "R":     0xFF^(1<<8),
                        "L":     0xFF^(1<<9),
                        "X":     0xFF^(1<<10),
                        "Y":     0xFF^(1<<11),
                        }

    def send(self, button="None"):
        data = self.empty.copy()
        data[0] = self.buttons[button.upper()]
        data = bytes(data)
        self.socket.send(data)
    
    def press(self,button,delay=0.3):
        self.send(button=button)
        sleep(delay)
        self.send(button="None")

    