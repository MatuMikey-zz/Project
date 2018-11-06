import csv
with open('SmallHouseNeuralNetwork.csv', 'r') as csvfile:
    so = csv.reader(csvfile, delimiter=';', quotechar='"')
    so = list(so)
import matplotlib.pyplot as plt

print (so)
sensor1=[]
sensor2=[]

for i in range(0, len(so)):
    sensor2.append(float(so[i][0]))    
    sensor1.append(float(so[i][1]))
    
plt.plot(sensor2)
plt.plot(sensor1)