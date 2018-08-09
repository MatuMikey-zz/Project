import serial
import time
import datetime
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
                    
                    print(character)
                    i = 20
                    mode = "write"
        elif mode=="write":
            time.sleep(0.1)
            ser.write("AT+CIPSEND=0,6\r\n".encode())
            time.sleep(0.1)
            ser.write(sentBytes+"\r\n".encode())
            
            mode = "read"
    except:
        print(character)
        continue;