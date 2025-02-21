from func import bmp
from func import MPU6050
from func import hv4pt
from func import server
import helper

import time
import csv
import datetime
import os
import RPi.GPIO as GPIO

"""
--------------------PIN LAYOUT--------------------
USING PIN NAME

BMP280  | PI4:
SCK     | SCL1
SDI     | SDA1

MPU6050 | PI4:
SCL     | SCL1
SDA     | SDA1

GPS6MV2 | PI4:
RX      | TXD0
TX      | RXD0

HV4PT   | PI4:
USB     | TOP BLUE USB PORT

FIREFLY | PI4:
LED     | GPIO18

BUZZER  | PI4:
PIN     | GPIO26

"""

"""--------------------CONSTANTS--------------------"""
# Constants that won't be touched

FLIGHT_MIN = 50
SLEEP_TIME = 0.5

"""--------------------GLOBAL VARS------------------"""
# Global Variables that will be used across functions

LAUNCHED = False
APOGEE = 0
BEGIN_TIME = 0




def main():
    print("Execution Start!")
    server.start_website("Awaiting Command")
    # Will only continue after stuff
    
    # Start Execution
    helper.beep(helper.BUZZER_PIN, 3, 1)
    
    # Initialize Writer
    now = datetime.datetime.now().strftime("%c")
    now = now.replace(" ", "_")
    now = now.replace(":", "_")
    filename = f"{os.path.dirname(__file__)}/data/{now}.csv"
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    print("Writing to: ", filename)
    writer = csv.writer(open(filename, "w", newline=""))
    writer.writerow(["n", "Datetime (UTC)", "Timestamp (s)", "Altitude (m)", "Temperature (C)", "Longitude", "Latitude", "Acceleration X (g)", "Acceleration Y (g)", "Acceleration Z (g)", "Flag"])
    
    
    """ Before Launch """
    begin_time = time.time()
    altitude = 0
    n = 0
    while altitude < FLIGHT_MIN:
        data = helper.record_data(n, begin_time)
        altitude = data["altitude"]
        n = n + 1
        time.sleep(SLEEP_TIME)
        
        # Write to CSV
        writer.writerow([data["n"], data["datetime"], data["timestamp"], data["altitude"], data["temperature"], data["longitude"], data["latitude"], data["acc_x"], data["acc_y"], data["acc_z"], data["flag"]])
        
    
        
        
    
    
    
if __name__ == "__main__":
    main()

