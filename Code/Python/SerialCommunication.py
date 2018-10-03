import serial
import time
import datetime
import numpy as np
import csv
from pathlib import Path
import random as random

myFile = Path('BigHouse.csv')
if not myFile.exists():
    with open('BigHouse.csv','a', newline='') as csvfile:
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


while 1:
    try:
        if mode=="read":
            character=ser.read(1).decode('utf-8') #TODO: TIMEOUT CHECK
            if (len(character) == 0 and (allConnected == True)):
                retryCounter = retryCounter + 1
            if retryCounter == 3:
                mode = "write"
                retryCounter = 0
                print("Retrying to sensor: ", sensorID) #//TODO implement neural net for
                                                        #//the specific sensor node
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
                        print ("The adc sensor values are:", adcSensorValues)
                        numberOfReadingsTakenThisSession = numberOfReadingsTakenThisSession + 1
                        print ("")
                        print ("Number of Readings taken so far:", numberOfReadingsTakenThisSession)
                        print ("")
                        receivedValues[0] = datetime.datetime.today().weekday()+1
                        now = datetime.datetime.now()
                        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
                        receivedValues[1] = (now - midnight).seconds
                        with open('BigHouse.csv','a', newline='') as csvfile:
                            writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                            writer.writerow(receivedValues)
                        with open('BigHouseNeuralNetwork.csv', 'a', newline='') as csvfile:
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
                sentBytes[2] = adcSensorValues[0]#1st and 3rd sensor ADC values sent
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