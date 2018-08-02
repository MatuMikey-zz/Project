import serial
import time
ser = serial.Serial(
        port = "COM4",
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        )# open first serial port

myBuffer = []
mystring = ''
i=16
while 1:
    myBuffer.append(ser.read(i).decode('utf-8'))
    print (len(myBuffer), myBuffer, mystring)
    mystring = ''.join(myBuffer)
    print(mystring.find("hello"))
    if(mystring.find("hello") != -1):
        i = 14
        print ("I AM HERE 1" + " " + mystring)
        time.sleep(0.5)       # check which port was really used
        ser.write(str.encode("AT+CIPSEND=0,3\r\n"))
        time.sleep(0.5)
        ser.write(str.encode("bye\r\n"))
        time.sleep(0.5)
        mystring = ''
        myBuffer = []
        ser.flushInput() #clears the buffers
        ser.flushOutput()
        time.sleep(0.5)
    elif(mystring.find("bye") != -1):
        i = 16
        print ("I AM HERE 2" + " " + mystring)
        time.sleep(0.5)
        ser.write(str.encode("AT+CIPSEND=0,5\r\n"))
        time.sleep(0.5)
        ser.write(str.encode("hello\r\n"))
        time.sleep(0.5)
        mystring = ''
        myBuffer = []
        ser.flushInput() #clears the buffers
        ser.flushOutput()
        time.sleep(0.5)
    else:
        i = 16
        time.sleep(0.5)
        ser.write(str.encode("AT+CIPSEND=0,4\r\n"))
        time.sleep(0.5)
        ser.write(str.encode("what\r\n"))
        time.sleep(0.5)
        mystring = ''
        myBuffer = []
        ser.flushInput() #clears the buffers
        ser.flushOutput()
        time.sleep(0.5)
