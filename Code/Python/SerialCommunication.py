import serial
import time
import datetime
import numpy as np
ser = serial.Serial(
        port = "COM3",
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        #timeout = 5
        )# open first serial port

ser.flush()
ser.flushInput()
ser.flushOutput()
time.sleep(1)

mode = "read"
time.sleep(0.3)
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

while 1:
    try:
        if mode=="read":
            character=ser.read(1).decode('utf-8')
            if (character == "+"):
                character = ser.read(1).decode('utf-8')
                if (character == "I"):
                    i = 8
                    readGarbage = ser.read(7).decode('utf-8')
                    messageWiFiID = int(readGarbage[3]) #used for determining which sensor this

                    
                            #reading belongs to
                    messageLength = int(readGarbage[5])
                    readMessage = ser.read(messageLength)#.decode('utf-8')
                    sensorID = int(readMessage[0])
                    if (allConnected == False):
                        wifiArray.append([sensorID,messageWiFiID])
                        print("Length is: ", len(wifiArray))
                        if (len(wifiArray) == 2):
                            allConnected = True

                    sensorCMD = int(readMessage[1])
                    sensorReading = int(readMessage[2])*256 + int(readMessage[3])
                    #print (sensorReading)
                    adcValue = float(sensorReading)
                    print (adcValue)
                    if(adcValue != 0):
                        R_th = 1000.0/((1023.0/(1023-adcValue))-1.0)
                        T = round(1.0/((1.0/298.15)+(1.0/3800.0)*(np.log(R_th/1000.0)))-273.15, 2) 
                        print ("Temperature sensor " +str(sensorID)+": " + str(T))
                    else:
                        R_th = 0
                        T = 60
                        print("ADC value: "+ str(adcValue))
                        print("Resistance value: " + str(R_th))
                        print ("Temperature sensor " +str(sensorID)+": " + str(T))
                    if(allConnected):
                        mode = "write"
        elif mode=="write":
            time.sleep(3) #this line of code controls how quickly the system will ask for values
            print ("Sensor ID is: " + str(sensorID))
            if (sensorID == 0):
                print ("sensor 2")
                for i in range(0, len(wifiArray)):
                    if wifiArray[i][0] == 1:
                        currentWifiModule = str(wifiArray[i][1])
                        print("Current Wifi Module: " + str(currentWifiModule))

                print("AT+CIPSEND="+currentWifiModule+",8")
                ser.write(("AT+CIPSEND="+currentWifiModule+",8\r\n").encode()) #send request to Wifi ID
                
            elif (sensorID == 1):
                print("sensor 1")
                for i in range(0, len(wifiArray)):
                    if wifiArray[i][0] == 0:
                        currentWifiModule = str(wifiArray[i][1])
                        print("Current Wifi Module: " + str(currentWifiModule))
                print("AT+CIPSEND="+currentWifiModule+",8")
                ser.write(("AT+CIPSEND="+currentWifiModule+",8\r\n").encode()) #send request to Wifi ID
                
            time.sleep(0.1)
            ser.write(sentBytes+"\r\n".encode())
            
            mode = "read"
    except:
        #print(character)
        continue;