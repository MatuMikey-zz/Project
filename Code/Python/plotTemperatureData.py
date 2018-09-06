import csv
with open('TemperatureData.csv', 'r') as csvfile:
    so = csv.reader(csvfile, delimiter=';', quotechar='"')
    so = list(so)
import matplotlib.pyplot as plt
def meanFilter(array):
    newArray = []
    for i in range(3, len(array)-3):
        newArray.append((array[i-3]+array[i-2]+array[i-1] + array[i] + array[i+1]+array[i+2]+array[i+3])/7.0)
    return newArray



sensor1=[]
sensor2=[]
sensor3=[]
time=[]
for i in range(1, len(so)-20):
    time.append(float(so[i][1]))    
    sensor1.append(float(so[i][2]))
    sensor2.append(float(so[i][3]))
    sensor3.append(float(so[i][4]))
    
    
#plt.plot(sensor3)
sensor1 = meanFilter(sensor1)
sensor2 = meanFilter(sensor2)
sensor3 = meanFilter(sensor3)
plt.subplot(2,2,1)
plt.plot(sensor1)
plt.subplot(2,2,2)
plt.plot(sensor2)
plt.subplot(2,2,3)
plt.plot(sensor3)


