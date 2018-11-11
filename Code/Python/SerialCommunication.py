import serial
import time
import datetime
import numpy as np
import csv
from pathlib import Path
import random as random
from NeuralNetwork import NeuralNetwork
from KalmanFilter import KalmanFilter

myFile = Path('ProjectDemonstration.csv')
if not myFile.exists():
    with open('ProjectDemonstration.csv','a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Day", "Seconds", "Sensor 0", "Sensor 1", "Sensor2"])
    
ser = serial.Serial(
        port = "COM3",
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout = 3
        )# open first serial port

ser.flush()
ser.flushInput()
ser.flushOutput()
time.sleep(1)

mode = "read"
ser.write("AT+CIPMUX=1\r\n".encode())
time.sleep(0.5)
ser.write("AT+CIPSERVER=1,333\r\n".encode())
time.sleep(0.5)
sentBytes = bytearray([1,10,2,0,2,0,0,54,0]) #[Header, Length, parameters...., Tail]
readGarbage = 'a'
wifi_n = 0
allConnected = False
wifiArray = []
currentWifiModule = 0
sensorID = 0
retryCounter = 0
neuralNetworkReadings = [0,0]
receivedValues = [0,0,0,0,0]
readingsCounter = 0
numberOfReadingsTakenThisSession = 0
adcSensorValues = [2,0,0,0,2,0]
canImpute = False


####################################### NEURAL NETWORK INITIATION ########################################
sensor0_nn = NeuralNetwork(11,1)
sensor0_nn.setWeights([-0.106369, 0.991191, 0.103826, 0.858796, 0.862443, -0.619618, -0.283207, 0.841984, -0.055582, -0.886149, 0.335518, 0.142667, -0.157037, -0.325786, 0.592725, -0.813903, -0.01555, -0.089715, -0.527365, -0.38451, 0.735491, 0.301953, -0.351799, -0.522011, -0.948513, -0.236367, 0.206833, -0.287737, 0.502775, 0.235988, -0.971984, 0.767801, 0.118285, 0.462117, -0.710947, 0.788714, 0.885672, -0.144803, 0.255205, 0.989823, -0.411329, -0.305331, -0.682137, 0.060724, 0.126756])
sensor1_nn = NeuralNetwork(11,1)
sensor1_nn.setWeights([-0.896015, 0.424812, -0.482631, 0.819613, 0.44003, -0.801746, -0.950281, -0.110542, 0.321476, -0.288528, 0.712818, -0.437488, -0.934631, 0.854445, -0.097756, 0.497305, 0.40275, 0.784643, 0.173291, -0.761357, 0.439287, -0.219173, 0.183995, 0.783485, -0.198632, 0.804402, -0.39106, -0.370914, -0.074073, -0.009628, 0.390659, 0.323379, -0.1711, -0.482061, -0.246571, -0.47962, -0.553874, 0.748612, 0.992264, 0.443214, 0.543182, 0.073638, 0.579294, -0.637121, 0.633369])
sensor2_nn = NeuralNetwork(11,1)
sensor2_nn.setWeights([0.828258, 0.860156, -0.13262, -0.374219, -0.781664, -0.679882, 0.392311, 0.275229, 0.972788, 0.113164, -0.364549, -0.7528, -0.818745, 0.966108, 0.226102, 0.738713, -0.081344, -0.960653, -0.448619, -0.877383, -0.059711, 0.159083, 0.808391, -0.380205, -0.732286, 0.984417, 0.666204, -0.067083, 0.310915, -0.72256, -0.355244, 0.259967, 0.947753, 0.842685, -0.389991, -0.287127, 0.987791, 0.946473, -0.611796, -0.362968, 0.449409, -0.553734, 0.697132, 0.548999, 0.76394])

###################################### END OF NN INITIATION ##############################################

####################################### FILTER INITIATION ################################################

kFilter1 = KalmanFilter(1,1,0.01)
kFilter2 = KalmanFilter(1,1,0.01)
kFilter3 = KalmanFilter(1,1,0.01)

####################################### END FILTER INITIATION ############################################

#######################################         GUI INTERFACE #####################################

from tkinter import *

root = Tk()

import tkinter.ttk

tkinter.ttk.Separator(root, orient=VERTICAL).grid(column=1, row=0, rowspan=8, sticky='ns')
tkinter.ttk.Separator(root, orient=VERTICAL).grid(column=3, row = 0, rowspan=8, sticky='ns')
tkinter.ttk.Separator(root, orient=VERTICAL).grid(column=5, row = 0, rowspan=8, sticky='ns')
tkinter.ttk.Separator(root, orient=VERTICAL).grid(column=7, row = 0, rowspan=8, sticky='ns')



tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0 ,row=1, columnspan=10, sticky='ew')
tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=1, row=3, columnspan=10, sticky='ew')
tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=1, row=5, columnspan=10, sticky='ew')
tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=7, columnspan=10, sticky='ew')
tkinter.ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=8, columnspan=10, sticky='ew')



#Labels
sensorNumberLabel= Label(root, text="Sensor #", font = "Helvetica 10 bold").grid(row=0, column=0)
sensorReadingLabel = Label(root, text="Sensor Temperature", font = "Helvetica 10 bold").grid(row=0, column=2)
sensorNeuralNetworkLabel = Label(root, text="Virtual Sensor Temperature", font = "Helvetica 10 bold").grid(row=0,column=4)
sensorErrorDifferenceLabel = Label(root, text="Error %", font = "Helvetica 10 bold").grid(row=0,column=6)
sensorOnlineLabel = Label(root, text="Sensor Online", font = "Helvetica 10 bold").grid(row=0,column=8)

sensor1Label = Label(root, text="Sensor 0").grid(row=2,column=0)
sensor2Label = Label(root, text="Sensor 1").grid(row=4, column=0)
sensor3Label = Label(root, text="Sensor 2").grid(row=6, column=0)
historicalLabel = Label(root, text="Historical data", font = "Helvetica 10 bold").grid(row=9,column=0)
#Buttons
allTimeButton = Button(root, text = "Past week", font = "Helvetica 10 bold"). grid(row=9, column=2)

s1r = StringVar()
s2r = StringVar()
s3r = StringVar()
sensor1ReadingLabel = Label(root, textvariable=s1r).grid(row=2,column=2)
sensor2ReadingLabel = Label(root, textvariable=s2r).grid(row=4,column=2)
sensor3ReadingLabel = Label(root, textvariable=s3r).grid(row=6,column=2)

n1r = StringVar()
n2r = StringVar()
n3r = StringVar() 
neural1ReadingLabel = Label(root, textvariable=n1r).grid(row=2,column=4)
neural2ReadingLabel = Label(root, textvariable=n2r).grid(row=4,column=4)
neural3ReadingLabel = Label(root, textvariable=n3r).grid(row=6,column=4)

e1r = StringVar()
e2r = StringVar()
e3r = StringVar()
error1ReadingLabel = Label(root, textvariable=e1r).grid(row=2,column=6)
error2ReadingLabel = Label(root, textvariable=e2r).grid(row=4,column=6)
error3ReadingLabel = Label(root, textvariable=e3r).grid(row=6,column=6)

sensor1Online = StringVar()
sensor2Online = StringVar()
sensor3Online = StringVar()
sensor1Online.set("No")
sensor2Online.set("No")
sensor3Online.set("No")
sensor1OnlineLabel = Label(root, textvariable=sensor1Online).grid(row=2, column=8)
sensor2OnlineLabel = Label(root, textvariable=sensor2Online).grid(row=4, column=8)
sensor3OnlineLabel = Label(root, textvariable=sensor3Online).grid(row=6, column=8)

root.update()
#####################################################################################################



############################################## TEST DEFINITIONS ######################################
def impute0(receivedValues, val):
     input0 = (receivedValues[3]-20.19118966351491)/(31.606867486886042-20.19118966351491)
     input1 = (receivedValues[4]-22.439817194444)/(28.700364998168894-22.439817194444)
     now = datetime.datetime.now()
     midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
     secondsPastMidnight = float((now - midnight).seconds)
     secondsPastMidnight = secondsPastMidnight/86400.0
     input2 = secondsPastMidnight
     value = sensor0_nn.predict([input0, input1, input2])*(28.50871344191931-21.824025388801964)+21.824025388801964
     if (val == 0):
         print("Sensor 0 imputed value:", round(value,2))
         n1r.set(str(round(value,2)))
     else:
         print ("Sensor 0 MLP value:", value)
         n1r.set(str(value))
     sensorID = 0
     
     sensor1Online.set("No")
     root.update()
     return value
def impute1(receivedValues, val):
     input0 = (receivedValues[2]-21.824025388801964)/(28.50871344191931-21.824025388801964)
     input1 = (receivedValues[4]-22.439817194444)/(28.700364998168894-22.439817194444)
     now = datetime.datetime.now()
     midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
     secondsPastMidnight = float((now - midnight).seconds)
     secondsPastMidnight = secondsPastMidnight/86400.0
     input2 = secondsPastMidnight
     value = sensor1_nn.predict([input0, input1, input2])*(31.606867486886042-20.19118966351491)+20.19118966351491
     if(val == 0):
         print("Sensor 1 imputed value:", round(value,2))
         n2r.set(str(round(value,2)))
     else:
         print("Sensor 1 MLP value:", value)
         n2r.set(str(value))
     sensorID = 1
     
     sensor2Online.set("No")
     root.update()
     return value
def impute2(receivedValues, val):
     input0 = (receivedValues[2]-21.824025388801964)/(28.50871344191931-21.824025388801964)
     input1 = (receivedValues[3]-20.19118966351491)/(31.606867486886042-20.19118966351491)
     now = datetime.datetime.now()
     midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
     secondsPastMidnight = float((now - midnight).seconds)
     secondsPastMidnight = secondsPastMidnight/86400.0
     input2 = secondsPastMidnight
     value = sensor2_nn.predict([input0, input1, input2])*(28.700364998168894-22.439817194444)+22.439817194444
     if (val == 0):
         print("Sensor 2 imputed value:", round(value,2))
         n3r.set(str(round(value,2)))
     else:
         print("Sensor 2 MLP value:", value)
         n3r.set(str(value))
     sensorID = 2
     
     sensor3Online.set("No")
     root.update()
     return value
     
######################################################### END OF TEST DEFINITIONS ###############################





while 1:
    try:
        if mode=="read":
            character=ser.read(1).decode('utf-8') #TODO: TIMEOUT CHECK
            if (len(character) == 0 and (allConnected == True)):
                retryCounter = retryCounter + 1
            if retryCounter == 3:
                mode = "write"
                retryCounter = 0
                if(sensorID == 0):
                    print("Imputing sensor: 1") #instead of retry use neural net?
                    if(canImpute == True):
                        storeValue = impute1(receivedValues,0)
                        receivedValues[3] = storeValue
                        sensorID = 1
                        sensor2Online.set("No")
                        s2r.set("No reading")
                        e2r.set("N/A")
                        root.update()

                elif(sensorID == 1):
                    print("Imputing sensor: 2")
                    if(canImpute == True):
                         storeValue = impute2(receivedValues,0)
                         receivedValues[4] = storeValue
                         sensorID= 2
                         sensor3Online.set("No")
                         s3r.set("No reading")
                         e3r.set("N/A")
                         root.update()

                elif(sensorID == 2):
                    print("Imputing sensor: 0")
                    if(canImpute == True):
                         storeValue = impute0(receivedValues,0)
                         receivedValues[2] = storeValue
                         sensorID = 0
                         sensor1Online.set("No")
                         s1r.set("No reading")
                         e1r.set("N/A")
                         root.update()
                         
            if (character == "+"):
                character = ser.read(1).decode('utf-8') #TODO: TIMEOUT CHECK
                if (character == "I"):
                    i = 8
                    readGarbage = ser.read(7).decode('utf-8')#TODO: TIMEOUT CHECK
                    if(len(readGarbage)!= 7):
                        print("Retrying!!!\n\n")
                        mode = "write"
                        continue
                    #print ("Reading garbage:", readGarbage)
                    messageWiFiID = int(readGarbage[3]) #used for determining which sensor this                    #reading belongs to
                    messageLength = int(readGarbage[5])
                    readMessage = ser.read(messageLength)#.decode('utf-8')
                    #print ("Reading full message:", readMessage.decode('utf-8'))
                    sensorID = int(readMessage[0])
                    if (allConnected == False):#Assign initial WiFi ID's
                        print(sensorID)
                        wifiArray.append([sensorID,messageWiFiID])
                        print("Length is: ", len(wifiArray))
                        if (len(wifiArray) == 3): #change for debug purposes
                            allConnected = True
                    else: #If a module disconnects and reconnects with a different ID, assign it.
                        for i in range(len(wifiArray)):
                            if (wifiArray[i][0] == sensorID): 
                                if(wifiArray[i][1] != messageWiFiID):
                                    print("WiFi ID has changed for this module. Reassigning!")
                                    print("Old WiFi ID:", wifiArray[i][1])
                                    print("New WiFi ID:", messageWiFiID)
                                    wifiArray[i][1] = messageWiFiID
                                    for j in range(len(wifiArray)):
                                        if (wifiArray[j][1] == messageWiFiID and i != j):
                                            wifiArray[j][1] = 8 #//assign default case so that WiFi don't interfere
                    #TO DO: REASSIGN WiFi module ID if it changes for a sensor node

                    sensorCMD = int(readMessage[1])
                    sensorReading = int(readMessage[2])*256 + int(readMessage[3])
                    print("sensor ID:", sensorID)
                    if(allConnected == True):
                        neuralNetReading = float(readMessage[4]) + float(readMessage[5]/100.0)
                        #print("Sensor " + str(sensorID) + " MLP reading:", neuralNetReading)
                    
                    #print("Sensor reading is:", sensorReading)
                    #print (sensorReading)
                    
                    adcValue = float(sensorReading)
                    print ("Sensor " + str(sensorID) + " ADC reading: ", adcValue)
                    if(adcValue != 0):
                        R_th = 1000.0/((1023.0/(1023-adcValue))-1.0)
                        T = round(1.0/((1.0/298.15)+(1.0/3800.0)*(np.log(R_th/1000.0)))-273.15, 2) 
                        print ("Sensor " +str(sensorID)+" Temperature: " + str(T))
                        
                        if sensorID == 0:
                            receivedValues[2] = T
                            adcSensorValues[0] = readMessage[2]
                            adcSensorValues[1] = readMessage[3]
                            neuralNetworkReadings[0] = neuralNetReading
                            T = round(kFilter1.updateEstimate(T),2)
                            if(canImpute == True):
                                error1 = round(abs(impute0(receivedValues, 1) - T)/(T)*100.0, 2)
                                print("Sensor 0 error: " + str(error1))
                                e1r.set(str(error1))
                            print("Sensor 0 filtered temperature: " + str(T))
                            s1r.set(str(T))
                            sensor1Online.set("Yes")
                            root.update()
                        if sensorID == 1:
                            receivedValues[3] = T
                            adcSensorValues[2] = readMessage[2]
                            adcSensorValues[3] = readMessage[3]
                            T = round(kFilter2.updateEstimate(T),2)
                            if (canImpute == True):
                                error2 = round(abs(impute1(receivedValues, 1) - T)/(T)*100.0, 2)
                                print("Sensor 1 error: " + str(error2))
                                e2r.set(str(error2))
                            print("Sensor 1 filtered temperature: " + str(T))

                            s2r.set(str(T))
                            sensor2Online.set("Yes")
                            root.update()
                            #special case
                        if sensorID == 2:
                            receivedValues[4] = T
                            adcSensorValues[4] = readMessage[2]
                            adcSensorValues[5] = readMessage[3]
                            neuralNetworkReadings[1] = neuralNetReading
                            T = round(kFilter3.updateEstimate(T),2)
                            if(canImpute == True):
                                error3 = round(abs(impute2(receivedValues, 1) - T)/(T)*100.0, 2)
                                print("Sensor 2 error: " + str(error3))
                                e3r.set(str(error3))
                            print("Sensor 2 filtered temperature: " + str(T))
                            s3r.set(str(T))
                            sensor3Online.set("Yes")
                            root.update()
                    else:
                        R_th = 0
                        T = 60
                        print("ADC value: "+ str(adcValue))
                        print("Resistance value: " + str(R_th))
                        print ("Temperature sensor " +str(sensorID)+": " + str(T))
                    if(allConnected):
                        mode = "write"
                    readingsCounter = readingsCounter + 1
                    #print("readingsCounter: ", readingsCounter)
                    if readingsCounter == 3:
                        readingsCounter = 0
                        canImpute = True
                        print ("\nThe ADC sensor values are:", adcSensorValues)
                        numberOfReadingsTakenThisSession = numberOfReadingsTakenThisSession + 1
                        print ("Number of Readings taken this session:", numberOfReadingsTakenThisSession)
                        print ("")
                        receivedValues[0] = datetime.datetime.today().weekday()+1
                        now = datetime.datetime.now()
                        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
                        receivedValues[1] = (now - midnight).seconds
                        with open('ProjectDemonstration.csv','a', newline='') as csvfile:
                            writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                            writer.writerow(receivedValues)
                        with open('PrDemoNN.csv', 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile, delimiter = ';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                            writer.writerow(neuralNetworkReadings)

        elif mode=="write":
            #print ("Sensor ID is: " + str(sensorID))
            time.sleep(8) #this line of code controls how quickly the system will ask for values
            
            if (sensorID == 0):
                print ("\nSending Request to Sensor 1")#, datetime.datetime.now.strftime("%Y-%m-%d %H:%M"))
                sentBytes[2] = adcSensorValues[0]#1st and 3rd sensor ADC values sent
                sentBytes[3] = adcSensorValues[1]
                sentBytes[4] = adcSensorValues[4]
                sentBytes[5] = adcSensorValues[5]
                for i in range(0, len(wifiArray)):
                    if wifiArray[i][0] == 1:
                        currentWifiModule = str(wifiArray[i][1])
                ser.write(("AT+CIPSEND="+currentWifiModule+",10\r\n").encode()) #send request to Wifi ID
                
            elif (sensorID == 1):
                print("\nSending Request to Sensor 2")#, datetime.datetime.now.strftime("%Y-%m-%d %H:%M"))
                sentBytes[2] = adcSensorValues[0]#1st and 2nd sensor ADC values sent
                sentBytes[3] = adcSensorValues[1]
                sentBytes[4] = adcSensorValues[2]
                sentBytes[5] = adcSensorValues[3]
                for i in range(0, len(wifiArray)):
                    if wifiArray[i][0] == 2:
                        currentWifiModule = str(wifiArray[i][1])
                ser.write(("AT+CIPSEND="+currentWifiModule+",10\r\n").encode()) #send request to Wifi ID
            elif (sensorID == 2):
                print("\nSending Request to Sensor 0")#, datetime.datetime.now.strftime("%Y-%m-%d %H:%M"))
                sentBytes[2] = adcSensorValues[2]#2nd and 3rd sensor ADC values sent
                sentBytes[3] = adcSensorValues[3]
                sentBytes[4] = adcSensorValues[4]
                sentBytes[5] = adcSensorValues[5]
                for i in range(0, len(wifiArray)):
                    if wifiArray[i][0] == 0:
                        currentWifiModule = str(wifiArray[i][1])
                ser.write(("AT+CIPSEND="+currentWifiModule+",10\r\n").encode())
                #send request to Wifi ID
            now = datetime.datetime.now()
            midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
            secondsPastMidnight = int((now - midnight).seconds)
            sentBytes[8] = secondsPastMidnight%256
            secondsPastMidnight = secondsPastMidnight//256
            sentBytes[7] = secondsPastMidnight%256
            secondsPastMidnight = secondsPastMidnight//256
            sentBytes[6] = secondsPastMidnight

            time.sleep(0.1)
            ser.write(sentBytes+"\r\n".encode())
            print("Message sent!\n")
            mode = "read"
    except:
        #print(character)
        continue;
        
        
