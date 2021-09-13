import matplotlib.pyplot as plotter
import random as rand

num_sensors = 8
range_val1 = 400
range_val2 = 500
num_val_per_sen = 11
time = 11
increment = 1

if __name__ == '__main__':
    x_axis: list[int] = []
    for incr in range(0, time, increment):
        x_axis.append(incr)

    values = []
    for i in range(num_sensors):
        values.append([])
        for x in range(num_val_per_sen):
            values[i].append(rand.randint(range_val1, range_val2))

    my_subplotter = plotter.subplot()

    n = 0  # numbered sensor
    for sen_val in values:
        n += 1
        my_subplotter.plot(x_axis, sen_val, label=("Sen " + str(n)))

    plotter.xlabel("Time")
    plotter.ylabel("PPM")
    my_subplotter.legend()
    plotter.show()
