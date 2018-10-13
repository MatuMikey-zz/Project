import serial
import time
import datetime
import numpy as np
import csv
from pathlib import Path
import random as random
from NeuralNetwork import NeuralNetwork

myFile = Path('SmallHouseTest2.csv')
if not myFile.exists():
    with open('SmallHouseTest2.csv','a', newline='') as csvfile:
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

sensor0_nn = NeuralNetwork(11,1)
sensor0_nn.setWeights([-0.741947, 0.10865, -0.917069, -0.043419, -0.071788, 0.583109, -0.873406, -0.955431, -0.669452, 0.53893, 0.882166, -0.002254, -0.190269, -0.54435, -0.006973, 0.170325, 0.857426, 0.93273, 0.398152, 0.464894, 0.270166, -0.481522, 0.28613, -0.1097, -0.738364, 0.15657, 0.019439, -0.277087, -0.511011, 0.223816, -0.900556, -0.339753, 0.959467, -0.59858, -0.946482, -0.639005, 0.957031, 0.339973, -0.198417, -0.729839, -0.238092, -0.911799, 0.719746, -0.558893, 0.216505])
sensor1_nn = NeuralNetwork(11,1)
sensor1_nn.setWeights([-0.902996, 0.731469, 0.664865, -0.047573, -0.383194, 0.232808, -0.948432, -0.826925, 0.489381, -0.975063, 0.206757, 0.278257, 0.681532, 0.452683, -0.604822, -0.08811, -0.644612, -0.923498, 0.610767, 0.199639, -0.894164, 0.197704, -0.801248, 0.428146, 0.225566, 0.904857, 0.674321, -0.444767, 0.392545, 0.079719, 0.499795, -0.606821, 0.793029, 0.528658, 0.579795, -0.051808, -0.870972, 0.239547, -0.58585, -0.167541, 0.215449, 0.474262, -0.985018, -0.958319, -0.976624])
sensor2_nn = NeuralNetwork(11,1)
sensor2_nn.setWeights([-0.650728, 0.874079, 0.221358, -0.532183, 0.315071, -0.22637, 0.629424, 0.862007, 0.842712, -0.845488, -0.585345, 0.299074, 0.152458, -0.966347, -0.905045, -0.061071, 0.465811, 0.152396, -0.614683, 0.752302, -0.963321, 0.129389, 0.288831, -0.29805, 0.967142, 0.117365, 0.747457, 0.567277, 0.286438, -0.993243, -0.103275, 0.94832, 0.227738, 0.915113, -0.092631, 0.967381, 0.094096, 0.576577, -0.66247, -0.238389, 0.797494, 0.518634, 0.517056, -0.549664, 0.072626])
#initiate neural networks here


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
                         input0 = (receivedValues[2]-21.541071413197535)/(36.584528199197784-21.541071413197535)
                         input1 = (receivedValues[4]-22.72858779740199)/(32.85368195780572-22.72858779740199)
                         now = datetime.datetime.now()
                         midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
                         secondsPastMidnight = float((now - midnight).seconds)
                         secondsPastMidnight = secondsPastMidnight/86400.0
                         input2 = secondsPastMidnight
                         value = sensor1_nn.predict([input0, input1, input2])*(30.789709748218648-23.82983524759436)+23.82983524759436
                         print("Sensor 1 imputed value:", value)
                         sensorID = 1
                         
                elif(sensorID == 1):
                    print("Imputing sensor: 2")
                    if(canImpute == True):
                         input0 = (receivedValues[2]-21.541071413197535)/(36.584528199197784-21.541071413197535)
                         input1 = (receivedValues[3]-23.82983524759436)/(30.789709748218648-23.82983524759436)
                         now = datetime.datetime.now()
                         midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
                         secondsPastMidnight = float((now - midnight).seconds)
                         secondsPastMidnight = secondsPastMidnight/86400.0
                         input2 = secondsPastMidnight
                         value = sensor1_nn.predict([input0, input1, input2])*(32.85368195780572-22.72858779740199)+22.72858779740199
                         print("Sensor 2 imputed value:", value)
                         sensorID = 2
                elif(sensorID == 2):
                    print("Imputing sensor: 0")
                    if(canImpute == True):
                         input0 = (receivedValues[3]-23.82983524759436)/(30.789709748218648-23.82983524759436)
                         input1 = (receivedValues[4]-22.72858779740199)/(32.85368195780572-22.72858779740199)
                         now = datetime.datetime.now()
                         midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
                         secondsPastMidnight = float((now - midnight).seconds)
                         secondsPastMidnight = secondsPastMidnight/86400.0
                         input2 = secondsPastMidnight
                         value = sensor1_nn.predict([input0, input1, input2])*(36.584528199197784-21.541071413197535)+21.541071413197535
                         print("Sensor 0 imputed value:", value)
                         sensorID = 0
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
                                    print("WiFi has changed for this module. Reassigning!")
                                    print("Old WiFi:", wifiArray[i][1])
                                    print("New WiFi:", messageWiFiID)
                                    wifiArray[i][1] = messageWiFiID
                                    for j in range(len(wifiArray)):
                                        if (wifiArray[j][1] == messageWiFiID and i != j):
                                            wifiArray[j][1] = 8 #//assign default case so that WiFi don't interfere
                    #TO DO: REASSIGN WiFi module ID if it changes for a sensor node

                    sensorCMD = int(readMessage[1])
                    sensorReading = int(readMessage[2])*256 + int(readMessage[3])
                    if(allConnected == True):
                        neuralNetReading = float(readMessage[4]) + float(readMessage[5]/100.0)
                        print("Neural net reading:", neuralNetReading)
                    
                    #print("Sensor reading is:", sensorReading)
                    #print (sensorReading)
                    print("sensor ID:", sensorID)
                    adcValue = float(sensorReading)
                    print (adcValue)
                    if(adcValue != 0):
                        R_th = 1000.0/((1023.0/(1023-adcValue))-1.0)
                        T = round(1.0/((1.0/298.15)+(1.0/3800.0)*(np.log(R_th/1000.0)))-273.15, 2) 
                        print ("Temperature sensor " +str(sensorID)+": " + str(T))
                        if sensorID == 0:
                            receivedValues[2] = T
                            adcSensorValues[0] = readMessage[2]
                            adcSensorValues[1] = readMessage[3]
                            neuralNetworkReadings[0] = neuralNetReading
                        if sensorID == 1:
                            receivedValues[3] = T
                            adcSensorValues[2] = readMessage[2]
                            adcSensorValues[3] = readMessage[3]
                            #special case
                        if sensorID == 2:
                            receivedValues[4] = T
                            adcSensorValues[4] = readMessage[2]
                            adcSensorValues[5] = readMessage[3]
                            neuralNetworkReadings[1] = neuralNetReading
                    else:
                        R_th = 0
                        T = 60
                        print("ADC value: "+ str(adcValue))
                        print("Resistance value: " + str(R_th))
                        print ("Temperature sensor " +str(sensorID)+": " + str(T))
                    if(allConnected):
                        mode = "write"
                    readingsCounter = readingsCounter + 1
                    print("readingsCounter: ", readingsCounter)
                    if readingsCounter == 3:
                        readingsCounter = 0
                        canImpute = True
                        print ("The adc sensor values are:", adcSensorValues)
                        numberOfReadingsTakenThisSession = numberOfReadingsTakenThisSession + 1
                        print ("")
                        print ("Number of Readings taken so far:", numberOfReadingsTakenThisSession)
                        print ("")
                        receivedValues[0] = datetime.datetime.today().weekday()+1
                        now = datetime.datetime.now()
                        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
                        receivedValues[1] = (now - midnight).seconds
                        with open('SmallHouseTest2.csv','a', newline='') as csvfile:
                            writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                            writer.writerow(receivedValues)
                        with open('SmallHouseNeuralNetwork.csv', 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile, delimiter = ';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                            writer.writerow(neuralNetworkReadings)

        elif mode=="write":
            print ("Sensor ID is: " + str(sensorID))
            time.sleep(8) #this line of code controls how quickly the system will ask for values
            
            if (sensorID == 0):
                print ("Sending Request to Sensor 1")#, datetime.datetime.now.strftime("%Y-%m-%d %H:%M"))
                sentBytes[2] = adcSensorValues[0]#1st and 3rd sensor ADC values sent
                sentBytes[3] = adcSensorValues[1]
                sentBytes[4] = adcSensorValues[4]
                sentBytes[5] = adcSensorValues[5]
                for i in range(0, len(wifiArray)):
                    if wifiArray[i][0] == 1:
                        currentWifiModule = str(wifiArray[i][1])
                ser.write(("AT+CIPSEND="+currentWifiModule+",10\r\n").encode()) #send request to Wifi ID
                
            elif (sensorID == 1):
                print("Sending Request to Sensor 2")#, datetime.datetime.now.strftime("%Y-%m-%d %H:%M"))
                sentBytes[2] = adcSensorValues[0]#1st and 2nd sensor ADC values sent
                sentBytes[3] = adcSensorValues[1]
                sentBytes[4] = adcSensorValues[2]
                sentBytes[5] = adcSensorValues[3]
                for i in range(0, len(wifiArray)):
                    if wifiArray[i][0] == 2:
                        currentWifiModule = str(wifiArray[i][1])
                ser.write(("AT+CIPSEND="+currentWifiModule+",10\r\n").encode()) #send request to Wifi ID
            elif (sensorID == 2):
                print("Sending Request to Sensor 0")#, datetime.datetime.now.strftime("%Y-%m-%d %H:%M"))
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