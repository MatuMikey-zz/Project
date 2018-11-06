import csv
from KalmanFilter import KalmanFilter
with open('SmallHouse.csv', 'r') as csvfile:
    so = csv.reader(csvfile, delimiter=';', quotechar='"')
    so = list(so)
import matplotlib.pyplot as plt


sensor1 = []

for i in range(1, len(so)):
    sensor1.append(float(so[i][2]))
#for i in range(1, len(so)):
    #if (so[i][2]  == 0.0 or so[i][3] == 0.0 or so[i][4] == 0.0):
     #   so.pop(i)
q = 0.001
errorArray = []
qvalues = []
while (q<=1.001):
    kFilter1 = KalmanFilter(1,1,q)
    error = 0.0
    for j in range(0, len(sensor1)):
        error = error + abs((kFilter1.updateEstimate(sensor1[j]) - sensor1[j])) 
    errorArray.append(error/(float(len(sensor1))))
    qvalues.append(q)
    q = q+0.001
    print(q)
    
plt.plot(qvalues, errorArray)