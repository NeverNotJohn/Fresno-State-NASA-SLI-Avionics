import time
import board

import adafruit_bmp280

# Create sensor object, communicating over the board's default I2C bus
try:
	i2c = board.I2C()  # uses board.SCL and board.SDA
	bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c,address=0x77)
except Exception as e:
	print("Error: ", e)
	

# change this to match the location's pressure (hPa) at sea level

# Zero out sea level pressure for altitude calculations
def calibrate_BMP280():
	
	# Add try statement
	
    sum = 0
    n = 10
    for i in range(n):
        sum = sum + bmp280.pressure
        time.sleep(0.33)
    sum = sum / n
    bmp280.sea_level_pressure = sum
    
def read_temp():
    
    try:
        temp = bmp280.temperature
    except Exception as e:
        print("Error: ", e)
        temp = -1
    
    return temp

def read_pressure():
    
    try:
        p = bmp280.pressure
    except Exception as e:
        print("Error: ", e)
        p = -1

    return p

def read_altitude():
    
    try:
        alt = bmp280.altitude
    except Exception as e:
        print("Error: ", e)
        alt = -1
    
    return alt


""" Main function for debugging """

def main():
    print("calibrating BMP280")
    calibrate_BMP280()
    # Calibrate time
    initial = time.time()
    while True:
        print("\nTime: %0.1f s" % (time.time()-initial))
        print("Temperature: %0.1f C" % read_temp())
        print("Pressure: %0.1f hPa" % read_pressure())
        print("Altitude = %0.2f meters" % read_altitude())
        time.sleep(3)
    
if __name__ == "__main__":
    main()
