import serial
import time
import serial.tools.list_ports
import math

s = [port.device for port in serial.tools.list_ports.comports()]

ser = serial.Serial(s[1], 115200)
buffer = []

while True:
    input = str(ser.readline())

    try:
        tof1, tof2, light1, light2 = input.split("-")
        if (light1 == '1'):
            print("BLACK TAPE")
            buffer = []
        else:
            buffer.append(tof1)
    except:
        print("init stuff")
    
    print(buffer)