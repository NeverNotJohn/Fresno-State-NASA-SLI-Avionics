import serial
import time

ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)

while True:
    data = ser.readline().decode('utf-8', errors='ignore')
    print(data)
    time.sleep(0.1)  
    
