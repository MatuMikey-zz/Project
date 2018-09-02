import serial
import time
import datetime
import numpy as np
import csv

with open('TemperatureData.csv','w', newline='') as csvfile:
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
sentBytes = bytearray([1,8,1,32,32,33,33,60]) #[Header, Length, Command, parameters...., Tail]
readGarbage = 'a'
wifi_n = 0
allConnected = False
wifiArray = []
currentWifiModule = 0
sensorID = 0
retryCounter = 0

receivedValues = [0,0,0,0,0]
readingsCounter = 0
numberOfReadingsTakenThisSession = 0



while 1:
    try:
        if mode=="read":
            character=ser.read(1).decode('utf-8') #TODO: TIMEOUT CHECK
            if (len(character) == 0 and (allConnected == True)):
                retryCounter = retryCounter + 1
            if retryCounter == 1:
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
                    messageWiFiID = int(readGarbage[3]) #used for determining which sensor this                    
                            #reading belongs to
                    messageLength = int(readGarbage[5])
                    readMessage = ser.read(messageLength)#.decode('utf-8')
                    #print ("Reading full message:", readMessage.decode('utf-8'))
                    sensorID = int(readMessage[0])
                    if (allConnected == False):#Assign initial WiFi ID's
                        wifiArray.append([sensorID,messageWiFiID])
                        #print("Length is: ", len(wifiArray))
                        if (len(wifiArray) == 3):
                            allConnected = True
                    else: #If a module disconnects and reconnects with a different ID, assign it.
                        for i in range(len(wifiArray)):
                            if (wifiArray[i][0] == sensorID): 
                                if(wifiArray[i][1] != messageWiFiID):
                                    print("WiFi has changed for this module. Reassigning!")
                                    print("Old WiFi:", wifiArray[i][1])
                                    print("New WiFi:", messageWiFiID)
                                    wifiArray[i][1] = messageWiFiID
                    #TO DO: REASSIGN WiFi module ID if it changes for a sensor node

                    sensorCMD = int(readMessage[1])
                    sensorReading = int(readMessage[2])*256 + int(readMessage[3])
                    #print("Sensor reading is:", sensorReading)
                    #print (sensorReading)
                    adcValue = float(sensorReading)
                    print (adcValue)
                    if(adcValue != 0):
                        R_th = 1000.0/((1023.0/(1023-adcValue))-1.0)
                        T = round(1.0/((1.0/298.15)+(1.0/3800.0)*(np.log(R_th/1000.0)))-273.15, 2) 
                        print ("Temperature sensor " +str(sensorID)+": " + str(T))
                        if sensorID == 0:
                            receivedValues[2] = T
                        if sensorID == 1:
                            receivedValues[3] = T
                        if sensorID == 2:
                            receivedValues[4] = T
                    else:
                        R_th = 0
                        T = 60
                        print("ADC value: "+ str(adcValue))
                        print("Resistance value: " + str(R_th))
                        print ("Temperature sensor " +str(sensorID)+": " + str(T))
                    if(allConnected):
                        mode = "write"
                    readingsCounter = readingsCounter + 1
                    if readingsCounter == 3:
                        readingsCounter = 0
                        numberOfReadingsTakenThisSession = numberOfReadingsTakenThisSession + 1
                        print ("")
                        print ("Number of Readings taken so far:", numberOfReadingsTakenThisSession)
                        print ("")
                        receivedValues[0] = datetime.datetime.today().weekday()+1
                        now = datetime.datetime.now()
                        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
                        receivedValues[1] = (now - midnight).seconds
                        with open('TemperatureData.csv','a', newline='') as csvfile:
                            writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                            writer.writerow(receivedValues)

        elif mode=="write":
            time.sleep(10) #this line of code controls how quickly the system will ask for values
            print ("Sensor ID is: " + str(sensorID))
            print("Time is: " + str(datetime.datetime.now()))
            if (sensorID == 0):
                print ("Sending Request to Sensor 1")#, datetime.datetime.now.strftime("%Y-%m-%d %H:%M"))
                for i in range(0, len(wifiArray)):
                    if wifiArray[i][0] == 1:
                        currentWifiModule = str(wifiArray[i][1])
                        print("Current Wifi Module: " + str(currentWifiModule))
                ser.write(("AT+CIPSEND="+currentWifiModule+",8\r\n").encode()) #send request to Wifi ID
                
            elif (sensorID == 1):
                print("Sending Request to Sensor 2")#, datetime.datetime.now.strftime("%Y-%m-%d %H:%M"))
                for i in range(0, len(wifiArray)):
                    if wifiArray[i][0] == 2:
                        currentWifiModule = str(wifiArray[i][1])
                        print("Current Wifi Module: " + str(currentWifiModule))
                ser.write(("AT+CIPSEND="+currentWifiModule+",8\r\n").encode()) #send request to Wifi ID
            elif (sensorID == 2):
                print("Sending Request to Sensor 0")#, datetime.datetime.now.strftime("%Y-%m-%d %H:%M"))
                for i in range(0, len(wifiArray)):
                    if wifiArray[i][0] == 0:
                        currentWifiModule = str(wifiArray[i][1])
                        print("Current Wifi Module: " + str(currentWifiModule))
                ser.write(("AT+CIPSEND="+currentWifiModule+",8\r\n").encode()) #send request to Wifi ID
                
            time.sleep(0.1)
            ser.write(sentBytes+"\r\n".encode())
            
            mode = "read"
    except:
        #print(character)
        continue;