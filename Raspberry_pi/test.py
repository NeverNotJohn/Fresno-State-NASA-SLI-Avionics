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
from helper import *
import threading

"""--------------------CONTROL--------------------"""
# Set true if you wanna test it

BMP = True
GPS = True
BERRY = True


def main():
    
    # Calibrate
    
    calibrate()
    
    # Start Threads
    berry_thread = threading.Thread(target=berryIMU.read_imu_data)
    GPS_thread = threading.Thread(target=GPS6MV2.get_GPS)
    berry_thread.start()
    GPS_thread.start()
    
    # record a couple times
    n = 0
    begin_time = time.time()
    BMP_APOGEE = 0
    print("Starting")
    while n < 250:
        data = record_data(n, begin_time, None)
        altitude = data["altitude"]
        
        if altitude > BMP_APOGEE:
            BMP_APOGEE = altitude
        
        print(dic_to_string(data))
        time.sleep(0.04)
        n+=1
    
    # Transmit
    print("Transmitting")
    temperature = data["temperature"]
    roll = data["angle_x"]
    pitch = data["angle_y"]
    yaw = data["angle_z"]
    landing_time = time.strftime("%H:%M:%S")
    kv4pt.transmit_data(BMP_APOGEE, temperature, landing_time, MAX_VELOCITY, roll, pitch, yaw)

if __name__ == "__main__":
    main()
    
