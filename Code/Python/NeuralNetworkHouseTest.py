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
n1.setWeights([0.466379, 0.646768, -0.96037, 0.528297, -0.825954, 0.053566, -0.866837, -0.636151, -0.061526, -0.937679, 0.536714, 0.758106, 0.008172, 0.603385, 0.09012, -0.566884, -0.969787, -0.227913, -0.337138, -0.65252, 0.183686, -0.878977, 0.049722, 0.434629, 0.861626, -0.914799, 0.807644, -0.88241, 0.723436, 0.718566, -0.866368, 0.387118, -0.016414, 0.758006, -0.680818, -0.7685, -0.285468, 0.951519, -0.570487, -0.787577, 0.347707, 0.334617, 0.808346, -0.796794, -0.145915])#[-0.20131, 0.628047, 0.264524, -0.006508, -0.738194, -0.817838, 0.979234, -0.288169, 0.171521, 0.514317, 0.99935, -0.989018, -0.584825, 0.400521, 0.236143, -0.872032, -0.60576, 0.509211, 0.059522, 0.557491, 0.116392, 0.403505, 0.070212, -0.993626, 0.080712, -0.68737, 0.149302, 0.204234, -0.005379, -0.635735, 0.830051, 0.792163, -0.788816, 0.727343, -0.381553, -0.602524, 0.667375, -0.644026, -0.137348, 0.465388, 0.633855, -0.424604, -0.35406, 0.296916, 0.665858])
n2.setWeights([0.636875, 0.447898, 0.521805, 0.594035, 0.804317, 0.691991, 0.471861, 0.891148, -0.760853, 0.552957, -0.671541, 0.910454, -0.196107, 0.40705, -0.204331, 0.964559, -0.03002, -0.20117, 0.763833, -0.749402, 0.917018, 0.775952, -0.828738, 0.192581, 0.638861, -0.46671, -0.732428, 0.609935, -0.140043, -0.216945, -0.045103, -0.473355, 0.4116, -0.092798, 0.263452, 0.581916, 0.465749, -0.579395, 0.74732, 0.46996, -0.040078, -0.827574, 0.363934, 0.354752, 0.87533])#[-0.077056, 0.963585, 0.763291, 0.527125, 0.734397, 0.541346, 0.756724, -0.272287, 0.99851, 0.367801, 0.30008, -0.435357, 0.945002, 0.759896, 0.822861, 0.927863, 0.991709, 0.952281, 0.953443, 0.930682, 0.97484, 0.912432, 0.885421, 0.947218, 0.939522, 0.978324, 0.995328, 0.914078, 0.99876, 0.917224, 0.960732, 0.920519, 0.908532, 0.004584, 0.812469, 0.02326, -0.071762, -0.354053, -0.102942, 0.321988, 0.282388, 0.260957, 0.729317, 0.849439, 0.926509])
n3.setWeights([0.75976, 0.611806, -0.196589, 0.02694, -0.308901, -0.508233, 0.889202, -0.8225, 0.899751, 0.469493, -0.72436, -0.561461, 0.808039, 0.520952, 0.617908, 0.565993, 0.111856, -0.348385, -0.509699, -0.906853, 0.731714, 0.167549, 0.156086, -0.73208, -0.885859, -0.511563, 0.219172, -0.538082, -0.787857, 0.421897, -0.629865, -0.912799, -0.810666, 0.910114, 0.088596, 0.809089, -0.157569, 0.964924, -0.473989, -0.370713, -0.044329, 0.593478, -0.746676, 0.959599, -0.113663])#[-0.636662, 0.537255, 0.089861, -0.061147, 0.211103, -0.391286, 0.955261, -0.972987, 0.777469, 0.676124, 0.524965, -0.433177, 0.592541, 0.057855, 0.37862, 0.111368, -0.803452, -0.232235, 0.703312, -0.081949, -0.253356, -0.125479, -0.100802, -0.109749, -0.169933, 0.415512, -0.18069, -0.695441, -0.586414, -0.095114, 0.251849, -0.962918, 0.969218, -0.983882, 0.651736, -0.038451, 0.41337, 0.757353, 0.238676, 0.713091, 0.455944, 0.401661, -0.003161, -0.88371, 0.782642])

time1 = []
time2 = []
sensor1 = []
sensor2 = []
sensor3 = []
with open('HouseData.csv', 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=';', quotechar='"')
    data = list(data)
    for i in range(1, len(data)):
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
    output1[i] = output1[i]*(37.3-21.78)+21.78
    sensor1[i] = sensor1[i]*(37.3-21.78)+21.78
    
    output2[i]  = output2[i]*(29.9-24.59)+24.59
    sensor2[i] = sensor2[i]*(29.9-24.59)+24.59
    
    output3[i]  = output3[i]*(29.52-23.95)+23.95
    sensor3[i] = sensor3[i]*(29.52-23.95)+23.95
    
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
