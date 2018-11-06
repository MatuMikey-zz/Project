import csv
import datetime as datetime
from KalmanFilter import KalmanFilter
with open('ProjectDemonstration.csv', 'r') as csvfile:
    so = csv.reader(csvfile, delimiter=';', quotechar='"')
    so = list(so)
   
sensor1=[]
sensor2=[]
sensor3=[]
time=[]
day = []
for i in range(1, len(so)):
    day.append(float(so[i][0]))
    time.append(float(so[i][1]))    
    sensor1.append(float(so[i][2]))
    sensor2.append(float(so[i][3]))
    sensor3.append((sensor1[i-1]+sensor2[i-1])/2.0)
    
    
with open('ProjectDemonstrationFix.csv','a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';',
    quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Day", "Seconds", "Sensor 0", "Sensor 1", "Sensor2"])
    

for i in range (0, len(sensor3)):
    receivedvalues = [day[i],time[i],sensor1[i],sensor2[i],sensor3[i]]
    with open('ProjectDemonstrationFix.csv','a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(receivedvalues)
