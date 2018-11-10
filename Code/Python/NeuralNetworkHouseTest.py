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
n1.setWeights([0.90492, 0.10402, 0.547756, -0.962668, 0.231911, -0.373563, 0.943605, 0.74545, -0.537731, -0.540043, -0.933165, 0.574172, 0.353149, -0.797014, 0.56136, 0.541242, 0.034506, 0.527748, -0.432595, 0.857761, 0.407225, -0.151148, 0.952997, 0.45702, 0.824225, -0.270999, -0.960794, -0.495707, -0.125724, -0.218374, 0.289334, -0.250397, 0.271993, 0.765415, 0.693533, 0.607448, -0.096737, -0.053988, 0.235932, 0.555194, -0.476538, -0.220726, -0.958439, -0.900953, -0.586565])
n2.setWeights([-0.753783, -0.660477, 0.22976, -0.449612, 0.496476, -0.07538, 0.41622, 0.599725, 0.585544, -0.497963, 0.899047, 0.44179, 0.946764, -0.436102, -0.490622, 0.376402, 0.306687, -0.267952, 0.592154, -0.878357, -0.53923, -0.014868, -0.145242, -0.123921, 0.161797, -0.675998, -0.043482, 0.92055, 0.21239, -0.365986, -0.943646, 0.955318, -0.510044, -0.893743, -0.524473, 0.229461, -0.23207, 0.044373, 0.148384, 0.596474, -0.74947, -0.349376, 0.377973, -0.971013, -0.009418])
n3.setWeights([0.759363, -0.211533, 0.166317, -0.803547, 0.709788, -0.696416, 0.067403, -0.534799, -0.073905, 0.411648, 0.013498, -0.303941, 0.631041, -0.112635, 0.487503, 0.31997, 0.434804, 0.410668, 0.793583, -0.612768, 0.30456, 0.853365, -0.308989, 0.232293, -0.868108, 0.220416, 0.071407, 0.337391, 0.593586, -0.271059, 0.163547, -0.687626, 0.612151, -0.53819, 0.835876, -0.94154, -0.599957, 0.548545, 0.876621, 0.041908, 0.540464, -0.6389, 0.993168, 0.275038, -0.459314])

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