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

mode = "write"
ser.write("AT+CIPMUX=1\r\n".encode())
time.sleep(0.5)
ser.write("AT+CIPSERVER=1,333\r\n".encode())
time.sleep(0.5)
sentBytes = bytearray([00,54,66,230,55,60])
readGarbage = 'a'

while 1:
    try:
        if mode=="read":
            character=ser.read(1).decode('utf-8')
            if (character == "+"):
                character = ser.read(1).decode('utf-8')
                if (character == "I"):
                    i = 8
                    readGarbage = ser.read(7).decode('utf-8')
                    messageWiFiID = readGarbage[3]
                    messageLength = int(readGarbage[5])
                    readMessage = ser.read(messageLength)#.decode('utf-8')
                    sensorID = int(readMessage[0])
                    sensorCMD = int(readMessage[1])
                    sensorReading = int(readMessage[2])*256 + int(readMessage[3])
                    #print (sensorReading)
                    adcValue = float(sensorReading)
                    print (adcValue)
                    if(adcValue != 0):
                        print("yeh")
                        R_th = 1000.0/((1023.0/(1023-adcValue))-1.0)
                        T = round(1.0/((1.0/298.15)+(1.0/3800.0)*(np.log(R_th/1000.0)))-273.15, 2) 
                        print("ADC value: "+ str(adcValue))
                        print("Resistance value: " + str(R_th))
                        print ("Temperature: " + str(T))
                    else:
                        R_th = 0
                        T = 60
                        print("ADC value: "+ str(ADC_Value))
                        print("Resistance value: " + str(R_th))
                        print ("Temperature: " + str(T))
                    #readWifiID = ser.read(1).decode('utf-8')
                    #print ("Reading wifi" + readWifiID)
                    #readGarbage = ser.read(1).decode('utf-8')
                    #print ("reading garbage: " + readGarbage)
                    #readMessageLength = ser.read(1).decode('utd-8')
                    #print("Reading message length: " + readMessageLength)
                    #readGarbage = ser.read(1)
                    #print ("Reading garbage: " + readGarbage)
                    #readMessage = ser.read(int(readMessageLength-1)).decode("utf-8")
                    
                    #print(readMessage)
                    #character=ser.read(7).decode('utf-8')
                    #character = ser.read(5).decode('utf-8')
                    #print (character)
                    """start1 =character.find("IPD,")+4
                    end2 = start1+1
                    WiFi_ID = character[start1:end2]
                    start = (character.find(WiFi_ID))+2
                    end = (character.find(":"))
                    Number_Of_Read_Characters = int(character[start:end])
                    character = ser.read(4).decode('utf-8')
                    ADC_Value = float(character)
                    if (ADC_Value != 0):
                        R_th = 1000.0/((1023.0/(1023-ADC_Value))-1.0)
                        T = round(1.0/((1.0/298.15)+(1.0/3800.0)*(np.log(R_th/1000.0)))-273.15, 2) 
                    else:
                        R_th = 0
                        T = 60
                    print("ADC value: "+ str(ADC_Value))
                    print("Resistance value: " + str(R_th))
                    print ("Temperature: " + str(T))
                    i = 20"""
                    mode = "write"
        elif mode=="write":
            time.sleep(3) #this line of code controls how quickly the system will ask for values
            ser.write("AT+CIPSEND=0,6\r\n".encode()) #send request to Wifi ID
            time.sleep(0.1)
            ser.write(sentBytes+"\r\n".encode())
            
            mode = "read"
    except:
        #print(character)
        continue;