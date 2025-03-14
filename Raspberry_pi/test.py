"""

Checks if all the sensors are working!

"""

import time
import math
from func import GPS6MV2
from func import bmp
from func import berryIMU
from func import server
from func import kv4pt

"""--------------------CONTROL--------------------"""
# Set true if you wanna test it

BMP = True
GPS = True
BERRY = True


def main():
    
    # Test BMP
    if BMP:
        print("Testing BMP")
        # Calibrate Test
        try:
            bmp.calibrate_BMP280()
            print("Calibration Successful!")
        except Exception as e:
            print("Error in Calibration: ", e)
        
        try:
            print("Temperature: ", bmp.read_temp())
            print("Pressure: ", bmp.read_pressure())
            print("Altitude: ", bmp.read_altitude())
        except Exception as e:
            print("Error in Reading: ", e)
            
        
