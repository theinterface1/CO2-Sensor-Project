import socket
import time
import json
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 10000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(7)
            if data:
                print( data.hex() )
                print( "CO2: " + (data[3] * 256 + data[4]).__str__())
            else:
                print('Connection with ', client_address, 'terminated')
                break

    finally:
        # Clean up the connection
        connection.close()
