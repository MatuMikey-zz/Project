from tkinter import *

root = Tk()

import tkinter.ttk

tkinter.ttk.Separator(root, orient=VERTICAL).grid(column=1, row=0, rowspan=8, sticky='ns')
tkinter.ttk.Separator(root, orient=VERTICAL).grid(column=3, row = 0, rowspan=8, sticky='ns')
tkinter.ttk.Separator(root, orient=VERTICAL).grid(column=5, row = 0, rowspan=8, sticky='ns')
tkinter.ttk.Separator(root, orient=VERTICAL).grid(column=7, row = 0, rowspan=8, sticky='ns')



tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0 ,row=1, columnspan=10, sticky='ew')
tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=1, row=3, columnspan=10, sticky='ew')
tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=1, row=5, columnspan=10, sticky='ew')
tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=7, columnspan=10, sticky='ew')
tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=8, columnspan=10, sticky='ew')



#Labels
sensorNumberLabel= Label(root, text="Sensor #", font = "Helvetica 10 bold").grid(row=0, column=0)
sensorReadingLabel = Label(root, text="Sensor Temperature", font = "Helvetica 10 bold").grid(row=0, column=2)
sensorNeuralNetworkLabel = Label(root, text="Neural Network Temperature", font = "Helvetica 10 bold").grid(row=0,column=4)
sensorErrorDifferenceLabel = Label(root, text="Error %", font = "Helvetica 10 bold").grid(row=0,column=6)
sensorOnlineLabel = Label(root, text="Sensor Online", font = "Helvetica 10 bold").grid(row=0,column=8)

sensor1Label = Label(root, text="Sensor 1").grid(row=2,column=0)
sensor2Label = Label(root, text="Sensor 2").grid(row=4, column=0)
sensor3Label = Label(root, text="Sensor 3").grid(row=6, column=0)
historicalLabel = Label(root, text="Historical data", font = "Helvetica 10 bold").grid(row=9,column=0)
#Buttons
allTimeButton = Button(root, text = "Past week", font = "Helvetica 10 bold"). grid(row=9, column=2)

while 1:
    root.update()