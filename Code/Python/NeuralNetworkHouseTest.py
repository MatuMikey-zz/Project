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
n1.setWeights([-0.153715, 0.164423, 0.330319, -0.610114, -0.642378, -0.982493, -0.747027, -0.444135, 0.770075, 0.273298, -0.747873, -0.995816, 0.585252, 0.481809, 0.262934, 0.900846, -0.631292, 0.943123, 0.658901, -0.558262, -0.229463, 0.375072, -7.7e-05, -0.991619, 0.101101, 0.048657, 0.518033, -0.019342, 0.974807, -0.930185, 0.84217, 0.833894, 0.976077, 0.731074, -0.436505, -0.749857, 0.447282, 0.250051, -0.652632, -0.506854, 0.714463, -0.781608, -0.145801, 0.138788, -0.612724])
n2.setWeights([-0.99639, -0.954398, -0.18814, -0.873413, -0.211008, 0.35114, -0.553564, -0.096986, -0.447506, -0.945995, -0.086601, -0.619426, -0.913524, -0.775755, -0.981632, -0.977238, -0.550635, -0.604988, -0.816707, -0.983051, -0.975626, -0.870962, -0.861339, -0.900366, -0.965061, -0.815547, -0.943636, -0.977468, -0.950746, -0.98822, 0.679052, 0.732704, 0.99983, 0.617737, -0.066434, -0.536102, -0.265036, -0.690879, -0.524027, 0.05221, -0.060823, 0.039311, -0.554001, 0.03851, 0.29264])
n3.setWeights([0.025109, 0.826858, -0.422511, -0.841391, -0.692457, 0.031479, -0.524101, -0.157857, 0.126817, 0.108123, -0.672357, 0.225217, 0.651608, 0.692555, -0.756144, -0.1321, 0.78279, 0.419592, -0.418242, -0.363828, 0.471385, -0.66003, 0.606088, -0.604228, -0.150985, 0.092078, 0.868753, -0.822377, -0.592201, -0.460164, -0.241226, 0.40243, -0.38061, 0.087367, -0.737068, -0.400113, -0.629363, 0.658825, 0.230358, -0.34268, -0.233642, -0.384457, -0.281614, -0.654162, -0.007324])

time1 = []
time2 = []
sensor1 = []
sensor2 = []
sensor3 = []
with open('SmallHouse.csv', 'r') as csvfile:
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
    output1[i] = output1[i]*(35.515-20.995)+20.995
    sensor1[i] = sensor1[i]*(35.515-20.995)+20.995
    
    output2[i]  = output2[i]*(28.981-24.372)+24.372
    sensor2[i] = sensor2[i]*(28.981-24.372)+24.372
    
    output3[i]  = output3[i]*(29.357-23.545)+23.95
    sensor3[i] = sensor3[i]*(29.357-23.545)+23.545
    
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
