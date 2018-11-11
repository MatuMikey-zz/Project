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
n1.setWeights([-0.106369, 0.991191, 0.103826, 0.858796, 0.862443, -0.619618, -0.283207, 0.841984, -0.055582, -0.886149, 0.335518, 0.142667, -0.157037, -0.325786, 0.592725, -0.813903, -0.01555, -0.089715, -0.527365, -0.38451, 0.735491, 0.301953, -0.351799, -0.522011, -0.948513, -0.236367, 0.206833, -0.287737, 0.502775, 0.235988, -0.971984, 0.767801, 0.118285, 0.462117, -0.710947, 0.788714, 0.885672, -0.144803, 0.255205, 0.989823, -0.411329, -0.305331, -0.682137, 0.060724, 0.126756])
n2.setWeights([-0.896015, 0.424812, -0.482631, 0.819613, 0.44003, -0.801746, -0.950281, -0.110542, 0.321476, -0.288528, 0.712818, -0.437488, -0.934631, 0.854445, -0.097756, 0.497305, 0.40275, 0.784643, 0.173291, -0.761357, 0.439287, -0.219173, 0.183995, 0.783485, -0.198632, 0.804402, -0.39106, -0.370914, -0.074073, -0.009628, 0.390659, 0.323379, -0.1711, -0.482061, -0.246571, -0.47962, -0.553874, 0.748612, 0.992264, 0.443214, 0.543182, 0.073638, 0.579294, -0.637121, 0.633369])
n3.setWeights([0.828258, 0.860156, -0.13262, -0.374219, -0.781664, -0.679882, 0.392311, 0.275229, 0.972788, 0.113164, -0.364549, -0.7528, -0.818745, 0.966108, 0.226102, 0.738713, -0.081344, -0.960653, -0.448619, -0.877383, -0.059711, 0.159083, 0.808391, -0.380205, -0.732286, 0.984417, 0.666204, -0.067083, 0.310915, -0.72256, -0.355244, 0.259967, 0.947753, 0.842685, -0.389991, -0.287127, 0.987791, 0.946473, -0.611796, -0.362968, 0.449409, -0.553734, 0.697132, 0.548999, 0.76394])

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
d = datetime.datetime(2018,10,5, 11,00)
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
    output2[i]  = output2[i]*(30.789709748218648-23.82983524759436)+23.82983524759436
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