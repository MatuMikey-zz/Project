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
sentBytes = bytearray([1,8,1,32,32,33,33,60]) #[Header, Length, Command, parameters...., Tail]
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
                    messageWiFiID = int(readGarbage[3]) #used for determining which sensor this
                                                   #reading belongs to
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
                        print("ADC value: "+ str(adcValue))
                        print("Resistance value: " + str(R_th))
                        print ("Temperature: " + str(T))
                    mode = "write"
        elif mode=="write":
            time.sleep(3) #this line of code controls how quickly the system will ask for values
            ser.write("AT+CIPSEND=0,8\r\n".encode()) #send request to Wifi ID
            time.sleep(0.1)
            ser.write(sentBytes+"\r\n".encode())
            
            mode = "read"
    except:
        #print(character)
        continue;