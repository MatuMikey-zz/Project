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

############################################## BUTTON COMMAND DEFINITIONS ###############################
def plotGraphs():
    from NeuralNetworker import NeuralNetwork
    from NeuralNetworker import normalise
    import csv
    import matplotlib.pyplot as plt
    import datetime
    from KalmanFilter import KalmanFilter
    import numpy as np
    import time
    
    kFilter1 = KalmanFilter(1,1,0.01)
    kFilter2 = KalmanFilter(1,1,0.01)
    kFilter3 = KalmanFilter(1,1,0.01)
    n1 = NeuralNetwork(11,1)
    n2 = NeuralNetwork(11,1)
    n3 = NeuralNetwork(11,1)
    n1.setWeights([-0.741947, 0.10865, -0.917069, -0.043419, -0.071788, 0.583109, -0.873406, -0.955431, -0.669452, 0.53893, 0.882166, -0.002254, -0.190269, -0.54435, -0.006973, 0.170325, 0.857426, 0.93273, 0.398152, 0.464894, 0.270166, -0.481522, 0.28613, -0.1097, -0.738364, 0.15657, 0.019439, -0.277087, -0.511011, 0.223816, -0.900556, -0.339753, 0.959467, -0.59858, -0.946482, -0.639005, 0.957031, 0.339973, -0.198417, -0.729839, -0.238092, -0.911799, 0.719746, -0.558893, 0.216505])
    n2.setWeights([-0.902996, 0.731469, 0.664865, -0.047573, -0.383194, 0.232808, -0.948432, -0.826925, 0.489381, -0.975063, 0.206757, 0.278257, 0.681532, 0.452683, -0.604822, -0.08811, -0.644612, -0.923498, 0.610767, 0.199639, -0.894164, 0.197704, -0.801248, 0.428146, 0.225566, 0.904857, 0.674321, -0.444767, 0.392545, 0.079719, 0.499795, -0.606821, 0.793029, 0.528658, 0.579795, -0.051808, -0.870972, 0.239547, -0.58585, -0.167541, 0.215449, 0.474262, -0.985018, -0.958319, -0.976624])
    n3.setWeights([-0.650728, 0.874079, 0.221358, -0.532183, 0.315071, -0.22637, 0.629424, 0.862007, 0.842712, -0.845488, -0.585345, 0.299074, 0.152458, -0.966347, -0.905045, -0.061071, 0.465811, 0.152396, -0.614683, 0.752302, -0.963321, 0.129389, 0.288831, -0.29805, 0.967142, 0.117365, 0.747457, 0.567277, 0.286438, -0.993243, -0.103275, 0.94832, 0.227738, 0.915113, -0.092631, 0.967381, 0.094096, 0.576577, -0.66247, -0.238389, 0.797494, 0.518634, 0.517056, -0.549664, 0.072626])
    
    time1 = []
    time2 = []
    sensor1 = []
    sensor2 = []
    sensor3 = []
    accuracy1 = []
    accuracy2 = []
    accuracy3 = []
    with open('ProjectDemonstration.csv', 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=';', quotechar='"')
        data = list(data)
        for i in range(5, len(data)-5):
            for j in range(0, len(data[i])):
                data[i][j] = float(data[i][j])
            if (data[i][2] == 0.0 or data[i][3] == 0.0 or data[i][4] == 0.0):
                continue
            time1.append(data[i][1])
            time2.append(data[i][1] + 86399*(data[i][0]-3))
            sensor1.append(kFilter1.updateEstimate(data[i][2]))
            sensor2.append(kFilter2.updateEstimate(data[i][3]))
            sensor3.append(kFilter3.updateEstimate(data[i][4]))
    
    normalise(time1, sensor1, sensor2, sensor3)
        
    output1 = []
    output2 = []
    output3 = []
    addseconds = []
    k = 0
    for i in range(0, len(time1)):
        addseconds.append(k)
        k = k+30
    d = datetime.datetime(2018,9,17, 14,00)
    print (d)
    x = [d + datetime.timedelta(seconds=i) for i in addseconds]
    start = 0
    end = 0
    store1 = []
    store2 = []
    store3 = []
    for i in range(0, len(sensor1)):
       start = time.time()
       output1.append(n1.predict([sensor2[i], sensor3[i], time1[i]]))
       output2.append(n2.predict([sensor1[i], sensor3[i], time1[i]]))
       output3.append(n3.predict([sensor1[i], sensor2[i], time1[i]]))
       store1.append(time.time()-start)
    
    error1 = []
    error2 = []
    error3 = []
    counter = 0
    for i in range(0, len(output1)):
        output1[i] = output1[i]*(36.584528199197784-21.541071413197535)+21.541071413197535
        sensor1[i] = sensor1[i]*(36.584528199197784-21.541071413197535)+21.541071413197535
        error1.append(abs(output1[i]-sensor1[i]))
        output2[i]  = output2[i]*(30.789709748218648-23.82983524759436)+23.82983524759436-2.5
        sensor2[i] = sensor2[i]*(30.789709748218648-23.82983524759436)+23.82983524759436
        error2.append(abs(output2[i]-sensor2[i]))
        output3[i]  = output3[i]*(32.85368195780572-22.72858779740199)+22.72858779740199
        sensor3[i] = sensor3[i]*(32.85368195780572-22.72858779740199)+22.72858779740199
        error3.append(abs(output3[i]-sensor3[i]))
    
    plt.figure(6)
    plt.plot(x,output1, color='red', label = "VS reading")
    plt.xlabel("Time (date, hour)")
    plt.ylabel("Temperature (degrees Celcius)")
    plt.title("Sensor and neural network temperature readings over a 7 day period")
    plt.plot(x,sensor1, color = 'green', label = "Sensor reading")
    plt.legend(loc='upper left')
    
    plt.gcf().autofmt_xdate()
    
    plt.figure(7)
    plt.plot(x,output2, color='red', label = "VS reading")
    plt.plot(x,sensor2, color = 'green', label = "Sensor reading")
    plt.legend(loc='upper left')
    plt.xlabel("Time (date, hour)")
    plt.ylabel("Temperature (degrees Celcius)")
    plt.title("Sensor and neural network temperature readings over a 7 day period")
    plt.gcf().autofmt_xdate()
    
    plt.figure(8)
    plt.plot(x,output3, color='red', label = "VS reading")
    plt.plot(x,sensor3, color = 'green', label = "Sensor reading")
    plt.xlabel("Time (date, hour)")
    plt.ylabel("Temperature (degrees Celcius)")
    plt.title("Sensor and neural network temperature readings over a 7 day period")
    plt.legend(loc='upper left')
    
    plt.gcf().autofmt_xdate()
    
    acc1 = []
    acc2 = []
    acc3 = []
    
    for i in range (0, len(error1)):
        if(sensor1[i] <= 5.0 or sensor2[i] <= 5.0 or sensor3[i] <= 5.0):
            continue
        acc1.append(error1[i]/sensor1[i]*100)
        acc2.append(error2[i]/sensor2[i]*100)
        acc3.append(error3[i]/sensor3[i]*100)
    
    s1 = 100
    s2 = 100
    s3 = 100
    b1 = 0
    b2 = 0
    b3 = 0
    for i in range(0,len(acc1)):
        if (acc1[i] <= s1):
            s1 = acc1[i]
        if (acc2[i] <= s2):
            s2 = acc2[i]
        if (acc3[i] <= s3):
            s3 = acc3[i]
        if (acc1[i] >= b1):
            b1 = acc1[i]
        if (acc2[i] >= b2):
            b2 = acc2[i]
        if (acc3[i] >= b3):
            b3 = acc3[i]
    print("")
    print("Std dev VS 1:", np.std(error1))
    print("Average accuracy VS 1:",100- np.average(acc1))
    print("Best accuracy VS 1:",100- s1)
    print("Worst accuracy VS 1:",100- b1)
    print("")
    print("Std dev VS 2:", np.std(error2))
    print("Average accuracy VS 2:", 100-np.average(acc2))
    print("Best accuracy VS 2:", 100-s2)
    print("Worst accuracy VS 2:", 100-b2)
    print("")
    print("Std dev VS 3:", np.std(error3))
    print("Average accuracy VS 3:", 100-np.average(acc3))
    print("Best accuracy VS 3:", 100-s3)
    print("Worst accuracy VS 3:", 100-b3)
    
    print (store1)
#########################################################################################################

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
allTimeButton = Button(root, text = "Past week", font = "Helvetica 10 bold", command = plotGraphs). grid(row=9, column=2)

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
    
    
