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
sensorNeuralNetworkLabel = Label(root, text="Virtual Sensor Temperature", font = "Helvetica 10 bold").grid(row=0,column=4)
sensorErrorDifferenceLabel = Label(root, text="Error %", font = "Helvetica 10 bold").grid(row=0,column=6)
sensorOnlineLabel = Label(root, text="Sensor Online", font = "Helvetica 10 bold").grid(row=0,column=8)

sensor1Label = Label(root, text="Sensor 1").grid(row=2,column=0)
sensor2Label = Label(root, text="Sensor 2").grid(row=4, column=0)
sensor3Label = Label(root, text="Sensor 3").grid(row=6, column=0)
historicalLabel = Label(root, text="Historical data", font = "Helvetica 10 bold").grid(row=9,column=0)
#Buttons
allTimeButton = Button(root, text = "Past week", font = "Helvetica 10 bold"). grid(row=9, column=2)

s1r = StringVar()
s2r = StringVar()
s3r = StringVar()
sensor1ReadingLabel = Label(root, textvariable=s1r).grid(row=2,column=2)
sensor2ReadingLabel = Label(root, textvariable=s2r).grid(row=4,column=2)
sensor3ReadingLabel = Label(root, textvariable=s3r).grid(row=6,column=2)

n1r = StringVar()
n2r = StringVar()
n3r = StringVar() 
neural1ReadingLabel = Label(root, textvariable=n1r).grid(row=2,column=4)
neural2ReadingLabel = Label(root, textvariable=n2r).grid(row=4,column=4)
neural3ReadingLabel = Label(root, textvariable=n3r).grid(row=6,column=4)

e1r = StringVar()
e2r = StringVar()
e3r = StringVar()
error1ReadingLabel = Label(root, textvariable=e1r).grid(row=2,column=6)
error2ReadingLabel = Label(root, textvariable=e2r).grid(row=4,column=6)
error3ReadingLabel = Label(root, textvariable=e3r).grid(row=6,column=6)




i= 0
while 1:
    i= i+1
    s1r.set(str(i))
    s2r.set(str(i))
    s3r.set(str(i))
    n1r.set(str(i))
    n2r.set(str(i))
    n3r.set(str(i))
    e1r.set(str(i))
    e2r.set(str(i))
    e3r.set(str(i))
    root.update()