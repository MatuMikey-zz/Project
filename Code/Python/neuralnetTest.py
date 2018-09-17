from NeuralNetworker import NeuralNetwork
from NeuralNetworker import normalise
import csv
import matplotlib.pyplot as plt


n1 = NeuralNetwork(11,1)
n2 = NeuralNetwork(11,1)
n3 = NeuralNetwork(11,1)
n1.setWeights([-0.007042, 0.628156, -0.426134, 0.35204, 0.187817, 0.969249, -0.75489, -0.646138, -0.63035, -0.226662, 0.234046, 0.194701, 0.48472, -0.82152, 0.751298, 0.842414, -0.851511, -0.561992, -0.438633, 0.802997, -0.51524, 0.396969, 0.146189, 0.061056, 0.903092, 0.463148, -0.936068, -0.07838, 0.607266, -0.738747, -0.749364, -0.055261, -0.432039, 0.340964, 0.80217, -0.563075, -0.862667, 0.316258, 0.364808, -0.308235, -0.064679, 0.566619, 0.917303, -0.469896, -0.938537])
n2.setWeights([0.066564, 0.237471, 0.184374, 0.961546, -0.856757, 0.921198, -0.525436, 0.000102, 0.658343, -0.844073, 0.79645, -0.673141, -0.907838, -0.831028, 0.917756, 0.947236, -0.891757, 0.228439, -0.667715, 0.906083, -0.843592, 0.370413, -0.434996, -0.749497, 0.254537, 0.199341, -0.351906, 0.974163, 0.699489, -0.141165, 0.869323, 0.928092, -0.349357, 0.759191, 0.999017, -0.432406, 0.482716, -0.8913, 0.953092, -0.706622, -0.151732, 0.476949, 0.580778, 0.26748, -0.362271])
n3.setWeights([0.013373, -0.915817, 0.412601, 0.823739, 0.469707, -0.46401, 0.339413, -0.214234, -0.694641, -0.585485, 0.684884, -0.820952, 0.361889, 0.837617, 0.064206, 0.690608, -0.536863, -0.048534, -0.905908, -0.410414, 0.408748, 0.557286, 0.354094, -0.893229, 0.363733, 0.903854, -0.653997, 0.756079, -0.588926, -0.818353, -0.524351, -0.796832, 0.826206, -0.64618, 0.209543, 0.749865, -0.737982, 0.389879, -0.864875, 0.035057, 0.539101, 0.24315, 0.023871, -0.893089, 0.695303])

time = []
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
        time.append(data[i][1])
        
        sensor1.append(data[i][2])
        sensor2.append(data[i][3])
        sensor3.append(data[i][4])
        

normalise(time, sensor1, sensor2, sensor3)
    
output1 = []
output2 = []
output3 = []
for i in range(0, len(sensor1)):
   output1.append(n1.predict([sensor2[i], sensor3[i], time[i]]))
   output2.append(n2.predict([sensor1[i], sensor3[i], time[i]]))
   output3.append(n3.predict([sensor1[i], sensor2[i], time[i]]))



for i in range(0, len(output1)):
    output1[i] = output1[i]*(34.61-20.08)+20.08
    sensor1[i] = sensor1[i]*(34.61-20.08)+20.08
    
    output2[i]  = output2[i]*(29.52-17.4)+17.4
    sensor2[i] = sensor2[i]*(29.52-17.4)+17.4
    
    output3[i]  = output3[i]*(60.25-11.91)+11.91
    sensor3[i] = sensor3[i]*(60.25-11.91)+11.91
    
    
plt.figure(6)
plt.plot(output1, color='red')
plt.plot(sensor1, color = 'green')

plt.figure(7)
plt.plot(output2, color='red')
plt.plot(sensor2, color = 'green')

plt.figure(8)
plt.plot(output3, color='red')
plt.plot(sensor3, color = 'green')

