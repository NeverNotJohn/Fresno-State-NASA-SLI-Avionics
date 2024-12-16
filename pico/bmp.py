from machine import Pin, I2C
from utime import sleep
from lib.bmp280_i2c import BMP280I2C

"""
User Defined Module for BMP280
"""


"""
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
bmp = BMP280I2C(i2c)

while True:
    temperature = bmp.temperature
    pressure = bmp.pressure
    print(f"Temperature: {temperature} C")
    print(f"Pressure: {pressure} Pa")
    sleep(1)
    
"""

def read_altitude():
    return 0

def read_temp():
    return 0

def read_pressure():
    return 0

def hello():
    while True:
        print("Hello World!")
        sleep(1)














    
def main():
    
    led = Pin(25, Pin.OUT)

    while True:
        led.value(not led.value())
        sleep(1)
    
if __name__ == "__main__":
    main()