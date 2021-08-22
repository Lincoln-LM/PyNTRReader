# Go to root of PyNTRReader
import sys
sys.path.append('../')

from ntrreader import G6Reader
from time import sleep

def getvalue(msg, key, digits=8):
    try:
        msg.index(key)
    except:
        return
    return int(msg[msg.index(key)+3:msg.index(key)+digits+3],16)

client = G6Reader('192.168.0.87', debug=True)
client.bpadd(0x125EC8)
client.bpadd(0x175CEC)
# client.bpdis(3)
while True:
    client.send_heartbeat_packet()
    r = str(client.socket.recv(1024))
    a = getvalue(r,"r0:")
    if a == 0x8c59e44:
        print(hex(getvalue(r,"r1:")))
        client.bpdis(3)
        client.bpdis(4)
    client.resume()
    sleep(0.1)