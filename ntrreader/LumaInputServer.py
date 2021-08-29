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
                        "NONE":  0xFFF,
                        "A":     0xFFF & ~(1<<0),
                        "B":     0xFFF & ~(1<<1),
                        "SELECT":0xFFF & ~(1<<2),
                        "START": 0xFFF & ~(1<<3),
                        "RIGHT": 0xFFF & ~(1<<4),
                        "LEFT":  0xFFF & ~(1<<5),
                        "UP":    0xFFF & ~(1<<6),
                        "DOWN":  0xFFF & ~(1<<7),
                        "R":     0xFFF & ~(1<<8),
                        "L":     0xFFF & ~(1<<9),
                        "X":     0xFFF & ~(1<<10),
                        "Y":     0xFFF & ~(1<<11),
                        }

    def send(self, buttons=[]):
        data = self.empty.copy()
        hidpad = 0xFFF
        for button in buttons:
            hidpad &= self.buttons[button.upper()]
        data[0] = hidpad & 0xFF
        data[1] = hidpad >> 8
        data = bytes(data)
        self.socket.send(data)
    
    def press(self,buttons,delay=0.3):
        self.send(buttons=buttons)
        sleep(delay)
        self.send()
    
    def touch(self, x, y,delay=0.3):
        data = self.empty.copy()
        x = (x * 4096) // 320
        y = (y * 4096) // 240
        touch_state = x | (y << 12) | (0x01 << 24)
        data[7] = touch_state >> 24
        data[6] = (touch_state >> 16) & 0xFF
        data[5] = (touch_state >> 8) & 0xFF
        data[4] = touch_state & 0xFF
        data = bytes(data)
        self.socket.send(data)
        sleep(delay)
        self.send()
