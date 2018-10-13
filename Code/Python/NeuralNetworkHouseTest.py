from NeuralNetworker import NeuralNetwork
from NeuralNetworker import normalise
import csv
import matplotlib.pyplot as plt
import datetime
from KalmanFilter import KalmanFilter

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
with open('SmallHouseTest2.csv', 'r') as csvfile:
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
for i in range(0, len(sensor1)):
   output1.append(n1.predict([sensor2[i], sensor3[i], time1[i]]))
   output2.append(n2.predict([sensor1[i], sensor3[i], time1[i]]))
   output3.append(n3.predict([sensor1[i], sensor2[i], time1[i]]))



for i in range(0, len(output1)):
    output1[i] = output1[i]*(36.584528199197784-21.541071413197535)+21.541071413197535
    sensor1[i] = sensor1[i]*(36.584528199197784-21.541071413197535)+21.541071413197535
    
    output2[i]  = output2[i]*(30.789709748218648-23.82983524759436)+23.82983524759436
    sensor2[i] = sensor2[i]*(30.789709748218648-23.82983524759436)+23.82983524759436
    
    output3[i]  = output3[i]*(32.85368195780572-22.72858779740199)+22.72858779740199
    sensor3[i] = sensor3[i]*(32.85368195780572-22.72858779740199)+22.72858779740199
    
plt.figure(6)
plt.plot(output1, color='red')
plt.xlabel("Time (days)")
plt.ylabel("Temperature (degrees Celcius)")
plt.title("Sensor and neural network temperature readings over a 5 day period")
plt.plot(sensor1, color = 'green')

plt.figure(7)
plt.plot(output2, color='red')
plt.plot(sensor2, color = 'green')
plt.xlabel("Time (days)")
plt.ylabel("Temperature (degrees Celcius)")
plt.title("Sensor and neural network temperature readings over a 5 day period")

plt.figure(8)
plt.plot(output3, color='red')
plt.plot(sensor3, color = 'green')
plt.xlabel("Time (days)")
plt.ylabel("Temperature (degrees Celcius)")
plt.title("Sensor and neural network temperature readings over a 5 day period")
