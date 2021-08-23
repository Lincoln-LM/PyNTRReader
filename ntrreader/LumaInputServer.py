import builtins
import socket
from time import sleep
class LumaInputServer():
    def __init__(self, server, port=4950):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = 4950
        self.socket.connect((server, port))
        self.empty = [0xFF, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x08, 0x80, 0x00]
        	# A
	        # B
	        # SELECT
	        # START
	        # DPADRIGHT
	        # DPADLEFT
	        # DPADUP
	        # DPADDOWN
	        # R
	        # L
	        # X
	        # Y
        self.buttons = {
                        "NONE":0xFF,
                        "A":0xFE,
                        "B":0xFD,
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

    