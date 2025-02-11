from machine import Pin, I2C
from utime import sleep
from lib.bmp280_i2c import BMP280I2C
import math

"""
User Defined Module for BMP280
"""   

class BMP280:
    def __init__(self, sda_pin=8, scl_pin=9, address=0x77):
        i2c0_sda = Pin(sda_pin)
        i2c0_scl = Pin(scl_pin)
        i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
        self.bmp280 = BMP280I2C(address, i2c0)
        self.sea_level_pressure = 1013.25
        
    def calibrate(self):
        total = 0
        for i in range(5):
            total += self.bmp280.measurements['p']
            sleep(1)
        self.sea_level_pressure = total / 5
        print("Calibrated to: ", self.sea_level_pressure)
        
    def read_values(self):
        readout = self.bmp280.measurements
        pressure = readout['p']
        temperature = readout['t']
        altitude = 44330 * (1.0 - math.pow((pressure / self.sea_level_pressure), 0.1903))
        return altitude, temperature, pressure


def main():

    yassss = BMP280()
    print("Calibrating...")
    yassss.calibrate()

    while True:
        data = yassss.read_values()
        print("Altitude: ", data[0])
        print("Temperature: ", data[1])
        print("Pressure: ", data[2])

    
if __name__ == "__main__":
    main()



