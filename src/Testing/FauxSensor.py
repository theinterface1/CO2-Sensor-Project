import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("10.0.0.183", 10000)

sock.connect(server_address)

data = [0xff, 0xff, 0xff, 0x01, 0x90, 0xff, 0xff]
vara = [0x94, 0xa0, 0x98, 0x96, 0x90, 0x9a, 0x9f, 0x94, 0xa0, 0x98, 0x96, 0x90, 0x9a, 0x9f]
for x in range(0,120):
    sock.recv(7)
    data[4] = vara[x % len(vara)]
    print(bytes(data))
    sock.sendall(bytes(data))

sock.close()