"""
Uri-Jaun Hall
CS 791
SensorCenter.py

This class handles receiving collected data and outputting to a window or file of choice.

The code after "if __name__ == "__main__":" mimics the entering of values into the
command line and allows running straight from the IDE

However if you wish to use the terminal this module can be ran by  running:
        python SensorCenter.py [RunTime] [Frequency] -t

        The -t signals this is a test run and uses a double array of integers for testing output.

        In near future -t will be optional. For now, the -t is necessary unless it is connected
        to a server, otherwise it calls the start() function which just waits for a connection


"""


from GraphicCenter import *
from SerialTransmitter import *
import time
import sys
import random as rand

FAIL = -1
SUCCESS = 0


class SensorCenter:
    def __init__(self):
        self.__file = ""                            # FILE FOR EXPORT
        self.__values = []                          # 2D ARRAY OF VALUES PER SENSOR
        self.graphic_center = GraphicCenter(self)   # HANDLES OUTPUT TO WINDOW
        self.__written = ""                         # OBJECT TO UPDATE FOR OUTPUT

        self.serial_transmitter = SerialTransmitter(self)       # HANDLES POLLING SENSORS
        self.pollFrequency = 1                      # frequency in seconds default = 1

    # ---------------------------------------------------
    # Start retrieving data
    # ---------------------------------------------------
    def start(self, comport):
        print('starting serial transmitter')
        serial_trans = self.serial_transmitter
        serial_trans.start(comport)

    # ----------------------------------------------------------------------
    # updates the data to be written based on double array values to CSV
    # --------------------------------------------------------------------
    def update_csv(self):
        self.__written = ""
        num_values = len(self.__values[0])
        num_sensors = len(self.__values)

        # Set title of columns
        self.__written = "Time"
        for name in self.serial_transmitter.namesAll():
            self.__written += ', ' + name
        self.__written += "\n\n"

        # Set values by column
        for i in range(num_values):
            self.__written += str(i+1)
            for intArr in self.__values:
                self.__written += "," + str(intArr[i])
            self.__written += "\n"

    # ---------------------------------------------------------------------
    # updates the data to be written based on double array values to window
    #   ( Same for now )
    # ---------------------------------------------------------------------
    def update(self):
        self.__written = ""
        num_values = len(self.__values[0])
        num_sensors = len(self.__values)

        # Set title of columns
        self.__written = "Time"
        for x in range(num_sensors):
            self.__written += "\tS" + str(x + 1)
        self.__written += "\n\n"

        # Set values by column
        for i in range(num_values):
            self.__written += str(i+1)
            for intArr in self.__values:
                self.__written += "\t" + str(intArr[i])
            self.__written += "\n"

    # --------------------------------------------
    # Routine to export data to a specified file
    # --------------------------------------------
    def export(self, file):
        try:
            self.__file = file
            print("\nProgram will output to " + str(file) + " file")
            file_writer = open(self.__file, "w")
            file_writer.write(self.__written)
            file_writer.close()
        except IOError as e:
            print("\nFile IO error:")
            print("\n" + e.strerror)
            return FAIL
        return SUCCESS

    # ---------------------------------------------------
    # --------------Getters and Setters------------------
    # --------------------------------------------------

    # ---------------------------------------------------
    # get value double array
    # ---------------------------------------------------
    def get_values(self):
        return self.__values

    # ---------------------------------------------------
    # add array of values
    # ---------------------------------------------------
    def add_sensor_values(self):
        pos = 0
        added = self.serial_transmitter.pollAll()
        for val in added:
            self.__values[pos].append(val)
            pos += 1

    # ---------------------------------------------------
    # add value to value array at index
    # ---------------------------------------------------
    def add_value_at_sensor(self, index, added):
        self.__values[index].append(added)

    # ----------------------------------------------------
    # get the set of values for specified sensor index
    # ----------------------------------------------------
    def get_sensor_values(self, index):
        return self.__values[index]

    # -----------------------------------------------------
    # get the value at index for specified sensor
    # -----------------------------------------------------
    def get_value_at_sensor(self, sensor, index):
        return self.get_sensor_values(sensor)[index]

    # -----------------------------------------------------
    # get output "self.written
    # -----------------------------------------------------
    def get_current_output(self):
        return self.__written

    # -----------------------------------------------------
    # returns the the length of the longest list in values
    # -----------------------------------------------------
    def get_longest_list(self):
        longest = 0
        for lis in self.__values:
            length = len(lis)
            if length > longest:
                longest = length
        return longest

    # -----------------------------------------------------
    # adds connected sensors to GUI
    # -----------------------------------------------------
    def update_sensor(self, sensor):
        self.graphic_center.add_sensor(sensor)


# ------------------------------------------------------------------
# ----------------------CLASS RUNNER CODE---------------------------
# ------------------------------------------------------------------


def main():

    # Create instance of SensorCenter
    center = SensorCenter()

    gc = center.graphic_center

    gc.out_to_window()


if __name__ == "__main__":
    main()
