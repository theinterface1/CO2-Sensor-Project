import time

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.figure as plotter
import matplotlib.pyplot as plt
import tkinter as tk
import matplotlib
import serial.tools.list_ports
from typing import List
from matplotlib.animation import FuncAnimation

matplotlib.use("TkAgg")


class GraphicCenter:

    def __init__(self, sensor_c):
        self.__sc = sensor_c
        self.window = tk.Tk()
        self.stopped = True
        print("\nInstance of the GraphicsCenter")

    # ---------------------------------------
    # Routine to create graph and export data to a window
    # ---------------------------------------
    def out_to_window(self):
        window = self.window
        window.title('CO2 Sensor Project')  # Title for Window
        window.geometry("1000x900")  # Size of window

        label_string = tk.StringVar()  # Needed to update text in window
        label_string.set(self.__sc.get_current_output())

        # def window_settings():  # Hoped to have another thread run this
        window.attributes('-topmost', True)
        window.update()
        window.attributes('-topmost', False)

        fig = plt.Figure(figsize=(4, 4), dpi=100)
        my_subplotter = fig.add_subplot()

        plt.show()

        # main panel
        panel_1 = tk.PanedWindow(bd=4, bg="black")
        panel_1.pack(fill=tk.BOTH, expand=1)

        # panel for sensors
        panel_2 = tk.PanedWindow(panel_1, orient=tk.VERTICAL, handlepad=16,
                                 handlesize=16, width=panel_1.winfo_screenwidth() / 7 + 8, bd=4)
        self.sensor_panel = panel_2

        # panel for graph and buttons
        panel_3 = tk.PanedWindow(panel_1, orient=tk.VERTICAL, handlepad=16,
                                 handlesize=16, bd=4, bg="black")

        # panel for graph
        panel_4 = tk.PanedWindow(panel_3, orient=tk.VERTICAL, bd=4,
                                 height=panel_3.winfo_screenheight() / 1.5)

        # add graph to canvas
        canvas = FigureCanvasTkAgg(fig, panel_4)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        def firstStart():
            if not self.stopped:
                return
            print("start")
            self.stopped = False
            self.animate(self.__sc.pollFrequency, window, my_subplotter, canvas)

        # panel for buttons
        button_frame = tk.Frame(window)
        panel_5 = tk.PanedWindow(panel_3, orient=tk.HORIZONTAL, bd=4, relief="raised")

        connect_but = tk.Button(button_frame, text="Connect", width=20,
                                command=lambda: self.__sc.start("COM3"))
        connect_but.grid(row=1, column=2, padx=(20, 20), pady=(5, 0))
        freq_txt = tk.Label(button_frame, text="Connection", font=("Helvetica", 11))
        freq_txt.grid(row=0, column=2, padx=(20, 20), pady=(0, 15))
        com_port = []

        for p in serial.tools.list_ports.comports():
            com_port.append(p.name)
        str_var = tk.StringVar(button_frame)
        if len(com_port) == 0:
            com_port.append("COM3")  # temporary port
        str_var.set(com_port[0])
        com_options = tk.OptionMenu(button_frame, str_var, *com_port)
        com_options.grid(row=0, column=2, pady=(55, 0))

        start_but = tk.Button(button_frame, text="Start", width=20,
                              command=firstStart)
        start_but.grid(row=0, column=3, padx=(20, 20), pady=(0, 18))

        stop_but = tk.Button(button_frame, text="Stop", width=20,
                             command=self.stop)
        stop_but.grid(row=0, column=3, padx=(20, 20), pady=(45, 0))

        freq = tk.Entry(button_frame, width=10)
        freq.grid(row=1, column=3, padx=(70, 0), pady=(0, 50))
        freq_txt = tk.Label(button_frame, text="Frequency s:", font=("Helvetica", 9))
        freq_txt.grid(row=1, column=3, padx=(0, 75), pady=(0, 50))
        freq_but = tk.Button(button_frame, text="Set", width=5,
                             command=lambda: self.set_freq(freq))
        freq_but.grid(row=1, column=3, pady=(5, 0))

        export_but = tk.Button(button_frame, text="Export", height=4, width=20,
                               command=lambda: self.export_window(window))
        export_but.grid(row=0, column=4, rowspan=2, pady=(4, 0), padx=(20, 20))

        pad = tk.Label(button_frame, text="            ")
        pad.grid(row=0, column=1)

        button_frame.pack()
        panel_5.add(button_frame)

        out = tk.Label(panel_2, textvariable=label_string, font=("Consolas", 10))

        # add matplotlib toolbar
        #        toolbar = NavigationToolbar2Tk(canvas, panel_4)
        #        toolbar.update()
        # canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        panel_2.add(out)
        panel_1.add(panel_2)
        #       panel_4.add(toolbar)
        panel_4.add(canvas.get_tk_widget())

        panel_3.add(panel_4)
        panel_3.add(panel_5)
        panel_1.add(panel_3)

        window.mainloop()

    # ---------------------------------------
    # Called repeatedly to update graph
    # ---------------------------------------
    def animate(self, i, window, pltr, canvas):
        if self.stopped:
            return
        self.__sc.add_sensor_values()
        x_axis = list(range(self.__sc.get_longest_list()))
        x_axis = list(map(lambda x: x * i, x_axis))

        pltr.cla()
        n = 0  # numbered sensor
        for sen_val in self.__sc.get_values():
            pltr.plot(x_axis, sen_val, label=self.__sc.serial_transmitter.namesAll()[n])
            n += 1

        pltr.set_xlabel("Time")
        pltr.set_ylabel("PPM")
        pltr.set_title('PPM/TIME')
        pltr.legend(loc='upper left')
        matplotlib.pyplot.tight_layout()

        canvas.draw()

        window.after(i * 1000, lambda: self.animate(i, window, pltr, canvas))

    # ---------------------------------------
    # Called when the export button is hit, opens a pop-up window with an entry field
    # ---------------------------------------
    def export_window(self, root):
        window = tk.Toplevel(root)

        label = tk.Label(window, text="File name")
        label.pack(fill='x', padx=50, pady=5)
        entry = tk.Entry(window)
        entry.pack(padx=5)

        b = tk.Button(window, text="OK", command=lambda: self.ok(entry, window))
        b.pack(pady=5)

    # ---------------------------------------
    # Called when the OK button is hit in the export pop-up window, takes the input and calls export
    # ---------------------------------------
    def ok(self, entry, window):
        e = entry.get()
        self.__sc.update_csv()
        self.__sc.export(e)
        window.destroy()

    # ---------------------------------------
    # Called when the rename button is hit, opens a pop-up window with an entry field
    # ---------------------------------------
    def rename_window(self, root, sensor, stingVar):
        window = tk.Toplevel(root)

        label = tk.Label(window, text="Sensor name")
        label.pack(fill='x', padx=50, pady=5)
        entry = tk.Entry(window)
        entry.pack(padx=5)

        b = tk.Button(window, text="OK", command=lambda: self.accept(entry, window, sensor, stingVar))
        b.pack(pady=5)

    # ---------------------------------------
    # Called when the OK button is hit in the export pop-up window, takes the input and calls export
    # ---------------------------------------
    def accept(self, entry, window, sensor, stringVar):
        e = entry.get()
        sensor.rename(e)
        stringVar.set(sensor.get_name())
        window.destroy()

    # ---------------------------------------
    # Called when the stop button is pressed to stop the real time graphing
    # ---------------------------------------
    def stop(self):
        self.stopped = True

    # ---------------------------------------
    # Called to set the polling frequency
    # ---------------------------------------
    def set_freq(self, entry):
        try:
            e = entry.get()
            self.__sc.pollFrequency = int(e)
        except Exception as e:
            print("Input value before setting frequency")

    # ---------------------------------------
    # Adds the connected sensors to the GUi
    # ---------------------------------------
    def add_sensor(self, sensor):
        sensor_frame = tk.Frame(self.window)
        sensor.frame = sensor_frame
        sensor_string = tk.StringVar()
        sensor_string.set(sensor.get_name())

        canvas = tk.Canvas(sensor_frame, relief="groove", bd=4, height=100)
        canvas.grid(row=0, column=0, pady=(5, 5))
        sensor_txt = tk.Label(canvas, textvariable=sensor_string,
                              font=("Helvetica", 12))  # need to get sensors names
        sensor_txt.grid(row=0, column=0, padx=(0, 10), pady=(7, 0))
        disconnect_but = tk.Button(canvas, text="Disconnect", width=15, command=lambda: sensor.delete_pan()
                                   )
        disconnect_but.grid(row=1, column=0, padx=(10, 5), pady=(5, 10))
        rename_but = tk.Button(canvas, text="Rename", width=15,
                               command=lambda: self.rename_window(self.window, sensor, sensor_string))
        rename_but.grid(row=1, column=1, padx=(5, 10), pady=(5, 10))

        self.sensor_panel.add(sensor_frame)

        '''
        def refresh():  # command to refresh data using updated array
            self.update()
            # Test Refresh
            self.written += "ADDED TO WINDOW"
            label_string.set(self.written)
    
        button_frame = tk.Frame(window)
        button_frame.pack()
        
        # Refresh Button
        refresh_button = tk.Button(button_frame, text="refresh", command=refresh)
        refresh_button.grid(row=100, column=100)
        button_frame.pack()
        # Windows starts and blocks process until closed
        # We may need another thread to get updates from the server
        '''
