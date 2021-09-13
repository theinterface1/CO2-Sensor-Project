import socket

import time

"""CO2 Sensor Project
CS791
Aurora Desmarais
Commented using PEP 257 Docstrings
"""


class ServerManager:
    """a server manager that handles the connection between the host system and the WiFi module

    Attributes:
    sensors : list of Sensor-s
        a list of the initialized Sensor-s that contain each of their socket information
    num_sensors : int
        an integer that contains the number of Sensor-s specified and that should be connected
    server_sock : socket
        the socket for the server
    """

    def __init__(self):
        """"initializes the server manager

        Arguments:
        self -- instance of the class SensorCenter.src.ServerManager
        """
        self.sensors = []
        self.num_sensors = 0
        self.server_sock = None

    def openServer(self, n):
        """"opens the TCP connection on the specified IP and port number 10000; initializes and connects to n number of sensors

        Arguments:
        self -- instance of the class SensorCenter.src.ServerManager
        n -- number of sensors
        """
        self.num_sensors = n

        try:
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # the first element of the tuple, the IP, must
            # be specified for each system it is on; '' is for the localhost IP
            self.server_sock.bind(('', 10000))
            self.server_sock.listen(5)
        except socket.error as e:
            print ("Server socket init error", e)
            exit(1)

        print("Server up")

        for i in range(0, self.num_sensors):
            try:
                sock, addr = self.server_sock.accept()
                s = Sensor(sock, addr)
                self.sensors.append(s)
                print ("Server and Sensor" + str(i) + " connected")
            except:
                print ("Client and Server connection error")
                exit(1)

    def pollAll(self):
        """"polls each

        Arguments:
        self -- instance of the class SensorCenter.src.ServerManager
        n -- number of sensors
        """
        results = []
        for s in self.sensors:
            results.append(s.poll())
        return results


class Sensor:
    """a sensor that contains the socket information for a sensor

    Attributes:
    sock : socket
        the socket between the sensor and the server
    addr : string
        address of the server
    """

    sensorCode = bytes([0xFE, 0X44, 0X00, 0X08, 0X02, 0X9F, 0X25])

    def __init__(self, s, a):
        """"initializes the Sensor

        Arguments:
        self -- instance of the class Sensor
        s -- socket between server and sensor
        a -- address of the server
        """
        self.sock = s
        self.addr = a

    def poll(self):
        """"polls the sensor and returns the data

        Arguments:
        self -- instance of the class Sensor
        """
        self.sock.sendall(self.sensorCode)
        result = self.sock.recv(7)
        hi = result[3]
        lo = result[4]
        ppm = (hi << 8) + lo
        return ppm


def main():
    """"main function that initializes the SensorCenter.src.ServerManager and polls the connected sensor, outputting the returned data
    """
    serverManager = ServerManager()
    serverManager.openServer(4)
    for i in range(5):
        results = serverManager.pollAll()
        for r in results:
            print(r)
        time.sleep(1)


if __name__ == "__main__":
    main()
