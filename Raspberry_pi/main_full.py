from func import bmp
from func import MPU6050
from func import kv4pt
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
    
    """ Variables """
    LAUNCHED = False
    BMP_APOGEE = 0
    BEGIN_TIME = 0
    
    
    """ Before Launch """
    begin_time = time.time()
    altitude = 0
    n = 0
    while altitude < FLIGHT_MIN:
        data = helper.record_data(n, begin_time, "Before Launch")
        altitude = data["altitude"]
        
        # Write to CSV
        writer.writerow([data["n"], data["datetime"], data["timestamp"], data["altitude"], data["temperature"], data["longitude"], data["latitude"], data["acc_x"], data["acc_y"], data["acc_z"], data["flag"]])
        
        # Indexing stuff
        n = n + 1
        time.sleep(SLEEP_TIME)
    
    """ During Launch """

    print("LIFTOFF!")
    ground_counter = 0
    
    while ground_counter < 10:      # bout 10 seconds of ground time
        data = helper.record_data(n, begin_time, "During Launch")
        altitude = data["altitude"]
        
        # Find BMP_APOGEE
        if altitude > BMP_APOGEE:
            BMP_APOGEE = altitude
        
        # Count Ground Time
        if altitude < FLIGHT_MIN:
            ground_counter += 1
            
        # Write to CSV
        writer.writerow([data["n"], data["datetime"], data["timestamp"], data["altitude"], data["temperature"], data["longitude"], data["latitude"], data["acc_x"], data["acc_y"], data["acc_z"], data["flag"]])
        
        # Indexing Stuff
        n = n + 1
        time.sleep(SLEEP_TIME)
        
    """ After Launch """
    print("TOUCHDOWN!")
    ground_counter = 0
    landing_time = time.strftime("%H:%M:%S")
    touch_down_time = time.time()
    print("Landing Time: ", landing_time)
    
    while int(time.time()) < int(touch_down_time + 300): # Execute for 300 seconds 
        
        # FIXME: Get Firefly Data
        
        # Record Temp
        data = helper.record_data(n, begin_time, "After Launch")
        temperature = data["temperature"]
        
        # Write to CSV
        writer.writerow([data["n"], data["datetime"], data["timestamp"], data["altitude"], data["temperature"], data["longitude"], data["latitude"], data["acc_x"], data["acc_y"], data["acc_z"], data["flag"]])
        
        # FIXME: Transmit Data
        kv4pt.transmit_data(BMP_APOGEE, temperature, landing_time, 1)
        
        # Indexing Stuff
        n = n + 1
        ground_counter += 1
        time.sleep(SLEEP_TIME)
        
        
    
    
    
if __name__ == "__main__":
    main()

