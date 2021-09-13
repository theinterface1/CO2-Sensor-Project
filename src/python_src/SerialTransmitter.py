import threading

import serial

import time

from typing import List

"""CO2 Sensor Project
CS791
Jordan Felt
Commented using PEP 257 Docstrings
"""


class SerialTransmitter:
    """a server manager that handles the connection between the host system and the WiFi module

    Attributes:
    sensors : list of Sensor-s
        a list of the initalized Sensor-s that contain each of their socket information
    num_sensors : int
        an integer that contains the number of Sensor-s specified and that should be connected
    server_sock : socket
        the socket for the server
    """

    def __init__(self, sensorCenter):
        """"initializes the server manager

        Arguments:
        self -- instance of the class SensorCenter.src.ServerManager
        """
        self.sensors = list()
        self.SSID = ""
        self.IP = ""
        self.COM = ""
        self.sc = sensorCenter

    def start(self, COM):
        self.COM = COM
        serialThread = threading.Thread(target=self.loop)
        serialThread.start()

    def loop(self):
        arduino_comm = serial.Serial(self.COM, 9600)

        while True:
            arduinoIn = arduino_comm.readline().decode()
            if "new " in arduinoIn:
                sensor_num: int = int(arduinoIn.split()[1])
                newSen = Sensor()
                newSen.rename("Sensor " + str(sensor_num))
                self.sensors.append(newSen)
                self.sc.get_values().append(list())
                self.sc.update_sensor(newSen)

            elif " sensor " in arduinoIn:
                split = arduinoIn.split()
                sensor_num: int = int(split[0])
                self.sensors[sensor_num].set_ppm(int(split[2]))
            elif "SSID:" in arduinoIn:
                self.SSID = arduinoIn.split()[1]
            elif "IP Address:" in arduinoIn:
                self.IP = arduinoIn.split()[2]

    def pollAll(self) -> List[int]:
        return list(map(lambda sen: sen.get_ppm(), self.sensors))

    def namesAll(self) -> List[str]:
        return list(map(lambda sen: sen.get_name(), self.sensors))


class Sensor:
    """a sensor that contains the socket information for a sensor

    Attributes:
    sock : socket
        the socket between the sensor and the server
    addr : string
        address of the server
    """

    def __init__(self):
        self.name: str = ""
        self.ppm: int = -1
        self.frame = None

    def set_ppm(self, val):
        self.ppm = val

    def get_ppm(self):
        return self.ppm

    def rename(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def delete_pan(self):
        self.frame.destroy()


def main():
    """"main function that initializes the SensorCenter.src.ServerManager and polls the connected sensor, outputting the returned data
    """
    serialTransmitter = SerialTransmitter(None)
    serialTransmitter.start("COM3")

    while True:
        time.sleep(1)
        for sensor in serialTransmitter.sensors:
            print(sensor.get_ppm(), end=" ")
        print('')


if __name__ == "__main__":
    main()
