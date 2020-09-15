import serial

import serial.tools.list_ports

s = [port.device for port in serial.tools.list_ports.comports()]

ser = serial.Serial(s[1])

while True:
    print(ser.readline())