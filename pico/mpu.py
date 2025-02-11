import machine
from lib.imu import MPU6050
from time import sleep
from machine import Pin, I2C

#Shows Pi is on by turning on LED when plugged in
LED = machine.Pin("LED", machine.Pin.OUT)
LED.on()

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

"""
--Units--

Temp: Degree Celsius
Accel: m/s^2
Gyro: Degrees per second?

"""

while True:
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x)
    gy=round(imu.gyro.y)
    gz=round(imu.gyro.z)
    tem=round(imu.temperature,2)
    
    print(f"Accel (x,y,z): {ax}, {ay}, {az}")
    print(f"Gyro (x,y,z): {gx}, {gy}, {gz}")
    print(f"Temperature: {tem}")
    
    print("\n")
    
    sleep(0.5) 