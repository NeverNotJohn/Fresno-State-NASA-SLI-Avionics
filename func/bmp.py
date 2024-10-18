import time
import board

import adafruit_bmp280

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c,address=0x76)

# change this to match the location's pressure (hPa) at sea level

# Zero out sea level pressure for altitude calculations
def calibrate_BMP280():
    sum = 0
    n = 10
    for i in range(n):
        sum = sum + bmp280.pressure
        time.sleep(0.33)
    sum = sum / n
    bmp280.sea_level_pressure = sum
    
def read_temp():
    return bmp280.temperature

def read_pressure():
    return bmp280.pressure

def read_altitude():
    return bmp280.altitude
    

try:
   while True:
      print("\nTemperature: %0.1f C" % bmp280.temperature)
      print("Pressure: %0.1f hPa" % bmp280.pressure)
      print("Altitude = %0.2f meters" % bmp280.altitude)
      time.sleep(2)
except KeyboardInterrupt:
    print("Exit")  # Exit on CTRL+C


""" Main function for debugging """

def main():
    print("calibrating BMP280")
    calibrate_BMP280()
    while True:
        print("\nTemperature: %0.1f C" % read_temp())
        print("Pressure: %0.1f hPa" % read_pressure)
        print("Altitude = %0.2f meters" % read_altitude())
        time.sleep(2)
    
if __name__ == "__main__":
    main()