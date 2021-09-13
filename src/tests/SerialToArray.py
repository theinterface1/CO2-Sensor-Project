import serial

import time

"""CO2 Sensor Project
CS791
Jordan Felt
Commented using PEP 257 Docstrings
"""

SSID = ""
IP = ""

arduino_comm = serial.Serial('COM3', 9600)

while True:
    arduinoIn = arduino_comm.readline().decode()
    if "sensor" in arduinoIn:

    elif "SSID:" in arduinoIn:
        SSID = arduinoIn[6:]
    elif "IP Address:" in arduinoIn:
        tp = arduinoIn[6:]
