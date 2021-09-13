import unittest
from src.python_src.SensorCenter import *


class SensorCenterTests(unittest.TestCase):

    def test_Confirm_Initial_Setup(self):
        run_time = 10
        freq = 2
        center = SensorCenter(run_time, freq)
        self.assertEqual(center.get_run_time(), run_time)
        self.assertEqual(center.get_poll_frequency(), freq)

    def test_Value_Add_and_Get(self):
        run_time = 10
        freq = 2
        num_sensors = 4

        center = SensorCenter(run_time, freq)
        for i in range(num_sensors):
            center.add_sensor_values([])

        center.add_value_at_sensor(0, 24)
        center.add_value_at_sensor(1, 25)
        center.add_value_at_sensor(2, 26)
        center.add_value_at_sensor(3, 27)

        self.assertEqual(center.get_value_at_sensor(0, 0), 24)
        self.assertEqual(center.get_value_at_sensor(1, 0), 25)
        self.assertEqual(center.get_value_at_sensor(2, 0), 26)
        self.assertEqual(center.get_value_at_sensor(3, 0), 27)

    def test_CSV_Output_Format(self):
        run_time = 10
        freq = 2
        num_sensors = 2

        center = SensorCenter(run_time, freq)
        for i in range(num_sensors):
            center.add_sensor_values([])

        center.add_value_at_sensor(0, 24)
        center.add_value_at_sensor(0, 25)
        center.add_value_at_sensor(0, 26)
        center.add_value_at_sensor(0, 27)
        center.add_value_at_sensor(1, 28)
        center.add_value_at_sensor(1, 29)
        center.add_value_at_sensor(1, 30)
        center.add_value_at_sensor(1, 31)
        myOutput = "Time\tS1\tS2\n\n1\t24\t28\n2\t25\t29\n3\t26\t30\n4\t27\t31\n"
        center.update()
        self.assertEqual(center.get_current_output(), myOutput)

    def test_Window_Output_Format(self):
        run_time = 10
        freq = 2
        num_sensors = 2

        center = SensorCenter(run_time, freq)
        for i in range(num_sensors):
            center.add_sensor_values([])

        center.add_value_at_sensor(0, 24)
        center.add_value_at_sensor(0, 25)
        center.add_value_at_sensor(0, 26)
        center.add_value_at_sensor(0, 27)
        center.add_value_at_sensor(1, 28)
        center.add_value_at_sensor(1, 29)
        center.add_value_at_sensor(1, 30)
        center.add_value_at_sensor(1, 31)
        myOutput = "Time,Sensor 1,Sensor 2\n\n1,24,28\n2,25,29\n3,26,30\n4,27,31\n"


if __name__ == "__main__":
    suite = unittest.TestSuite()
    classes = [SensorCenterTests]
    for c in classes:
       suite.addTests(unittest.TestLoader().loadTestsFromTestCase(c))

    r = unittest.TestResult()
    suite.run(r)
    if r.wasSuccessful():
        print("All tests passed.")
    else:
        print("Failed test traces:")
        for f in r.failures:
            for x in f: print(x)
        print("Errored test traces:")
        for f in r.errors:
            for x in f: print(x)

