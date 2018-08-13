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

myBuffer = []
mystring = ''
reading = False
character = 'a'
i=1
mode = "write"
ser.write("AT+CIPMUX=1\r\n".encode())
time.sleep(0.5)
ser.write("AT+CIPSERVER=1,333\r\n".encode())
time.sleep(0.5)
sentBytes = bytearray([00,54,66,230,55,60])
while 1:
    try:
        if mode=="read":
            character=ser.read(1).decode('utf-8')
            if (character == "+"):
                character = ser.read(1).decode('utf-8')
                if (character == "I"):
                    i = 8
                    character=ser.read(i).decode('utf-8')
                    start1 =character.find("IPD,")+4
                    end2 = start1+1
                    WiFi_ID = character[start1:end2]
                    start = (character.find(WiFi_ID))+2
                    end = (character.find(":"))
                    Number_Of_Read_Characters = int(character[start:end])
                    character = ser.read(4).decode('utf-8')
                    ADC_Value = float(character)
                    if (ADC_Value != 0):
                        print("weh")
                        R_th = 1000.0/((1023.0/(1023-ADC_Value))-1.0)
                        T = round(1.0/((1.0/298.15)+(1.0/3800.0)*(np.log(R_th/1000.0)))-273.15, 2) 
                    else:
                        print("weh2")
                        R_th = 0
                        T = 60
                    print("ADC value: "+ str(ADC_Value) + "\nResistance value: "+ str(R_th) + "\nTemperature: " + str(T))
                    i = 20
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