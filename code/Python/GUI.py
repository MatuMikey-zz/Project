from tkinter import *

root = Tk()

import tkinter.ttk

tkinter.ttk.Separator(root, orient=VERTICAL).grid(column=1, row=0, rowspan=7, sticky='ns')
tkinter.ttk.Separator(root, orient=VERTICAL).grid(column=3, row = 0, rowspan=7, sticky='ns')
tkinter.ttk.Separator(root, orient=VERTICAL).grid(column=5, row = 0, rowspan=7, sticky='ns')

tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=1, columnspan=8, sticky='ew')
tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=3, columnspan=8, sticky='ew')
tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=5, columnspan=8, sticky='ew')


sensorNumberLabel= Label(root, text="Sensor #", font = "Helvetica 10 bold").grid(row=0, column=0)
sensorReadingLabel = Label(root, text="Sensor Temperature", font = "Helvetica 10 bold").grid(row=0, column=2)
sensorNeuralNetworkLabel = Label(root, text="Neural Network Temperature", font = "Helvetica 10 bold").grid(row=0,column=4)
sensorOnlineLabel = Label(root, text="Sensor Online", font = "Helvetica 10 bold").grid(row=0,column=6)

sensor1Label = Label(root, text="Sensor 1").grid(row=2,column=0)
sensor2Label = Label(root, text="Sensor 2").grid(row=4, column=0)
sensor3Label = Label(root, text="Sensor 3").grid(row=6, column=0)


while 1:
    root.update()