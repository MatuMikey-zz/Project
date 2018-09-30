import csv
from KalmanFilter import KalmanFilter
with open('BigHouse.csv', 'r') as csvfile:
    so = csv.reader(csvfile, delimiter=';', quotechar='"')
    so = list(so)
import matplotlib.pyplot as plt

def meanFilter(array):
    newArray = []
    for i in range(3, len(array)-3):
        newArray.append((array[i-3]+array[i-2]+array[i-1] + array[i] + array[i+1]+array[i+2]+array[i+3])/7.0)
    return newArray


kFilter1 = KalmanFilter(1,1,0.01)
kFilter2 = KalmanFilter(1,1,0.01)
kFilter3 = KalmanFilter(1,1,0.01)
sensor1=[]
sensor2=[]
sensor3=[]
time=[]
#for i in range(1, len(so)):
    #if (so[i][2]  == 0.0 or so[i][3] == 0.0 or so[i][4] == 0.0):
     #   so.pop(i)
for i in range(1, len(so)):
    time.append(float(so[i][1]))    
    sensor1.append(float(so[i][2]))
    sensor2.append(float(so[i][3]))
    sensor3.append(float(so[i][4]))


plt.subplot(2,2,1)
plt.plot(sensor1)
plt.subplot(2,2,2)
plt.plot(sensor2)
plt.subplot(2,2,3)
plt.plot(sensor3)

for i in range(0, len(sensor1)):
    sensor1[i] = kFilter1.updateEstimate(sensor1[i])
    sensor2[i] = kFilter2.updateEstimate(sensor2[i])
    sensor3[i] = kFilter3.updateEstimate(sensor3[i])

plt.subplot(2,2,1)
plt.plot(sensor1)
plt.subplot(2,2,2)
plt.plot(sensor2)
plt.subplot(2,2,3)
plt.plot(sensor3)
   
#plt.plot(sensor3)


