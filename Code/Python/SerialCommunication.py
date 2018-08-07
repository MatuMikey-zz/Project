import serial
import time
ser = serial.Serial(
        port = "COM3",
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        #timeout = 5
        )# open first serial port

myBuffer = []
mystring = ''
reading = False
character = 'a'
i=1
mode = "read"
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
                    character = ser.read(Number_Of_Read_Characters).decode('utf-8')
                    print(character)
                    i = 20
        else:
            ser.write("AT+CIPSEND=0,1\r\n")
            time.sleep(0.5)
            ser.write("a\r\n")
            ser.sleep(0.5)
                #ser.flushInput()
            #if (i == 20):
                #time.sleep(1)
                #ser.write(str.encode("AT+CIPSEND=0,3\r\n"))
                #time.sleep(0.5)
                #ser.write(str.encode("bye\r\n"))
    except:
        continue;