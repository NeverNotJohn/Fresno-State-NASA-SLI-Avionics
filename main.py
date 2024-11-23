from func import bmp
from func import GPS
import time
import csv
import datetime
import os
import sys
import RPi.GPIO as GPIO

"""
Pins:

BMP280 -> PI4:
SCK -> 5
SDI -> 3

GPS6MV2 -> PI4:
TX -> 10

"""

#--------------------GPIO Setuppp--------------------
BUZZER_PIN = 6										# GPIO 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)


#--------------------Globals Vars--------------------
now = datetime.datetime.now().strftime("%c")
print(now)

filename = f"{os.path.dirname(__file__)}/data/{now}.csv"
print(filename)
writer = csv.writer(open(filename, "w", newline=""))



#--------------------Functions-----------------------

def beep(pin=6, duration=0.2, times=3):
	try:
		for i in range(times):
			GPIO.output(pin, GPIO.HIGH)
			time.sleep(duration)
			GPIO.output(pin, GPIO.LOW)
			time.sleep(duration)
	except Exception as e:
		print("Error: ", e)
	

def initialize():
    global writer
    global BUZZER_PIN
    
    print("Calibrating..")
    bmp.calibrate_BMP280()
    print("Calibrating...")
    GPS.calibrate_GPS()
    print("Calibrating Done!")
    
    beep(BUZZER_PIN)
    
    writer.writerow(["n", "timestamp (s)", "altitude (m)", "latitude", "longitude", "temperature (C)", "pressure (hPa)", "acceleration", "gyroscope", "battery", "Flags"])

def dic_to_string(data):
    string = ""
    for key, value in data.items():
        string += f"{key}: {value} "
    return string

def record_data(n, begin, flag=""):
    global writer
    
    # Beep if it works
    if n % 20 == 0:
		beep(BUZZER_PIN, 0.2, 1)
    
    altitude = round(bmp.read_altitude(),3)
    temperature = round(bmp.read_temp(),3)
    pressure = round(bmp.read_pressure(), 3)
    
    temp = GPS.get_GPS()
    latitude = temp[0]
    longitude = temp[1]
    
    # for Debug Reasons
    data = {
            "n": n, 
            "timestamp": round(time.time() - begin,3), 
            "altitude": altitude, 
            "latitude": latitude, 
            "longitude": longitude, 
            "temperature": temperature, 
            "pressure": pressure, 
            "acceleration": 0, 
            "gyroscope": 0, 
            "battery": 0,
            "Flags": flag
            }
    
    writer.writerow([n, round(time.time() - begin,3), altitude, latitude, longitude, temperature, pressure, 0, 0, 0, flag])
    string = dic_to_string(data)
    print(string, "\n")
    
    return data

#------------------------Main------------------------

def main():
	
    # Variables
    n = 0
    begin = time.time()
    launched = False
    landed = False
    flight_min = 50
    sleep_time = 0.5
	
    print("Calibrating.")
    initialize()
    
    # Before Launch
    altitude = 0
    while altitude < flight_min:
        altitude = bmp.bmp280.altitude
        record_data(n, begin)
        n += 1
        time.sleep(sleep_time)
    
    # Set Launch Bit to True and record on .csv
    launched = True
    print("Launch Detected")
    record_data(n, begin, "Launch Detected")
    
    # During Launch
    ground_counter = 0		# Counts how many points below 50m
    
    while ground_counter < 50:
        altitude = bmp.bmp280.altitude
        record_data(n, begin)
        n += 1
        time.sleep(sleep_time)
		
        if (altitude < flight_min):
            ground_counter = ground_counter + 1
			
	# Landed
    landed = True
    print("Touchdown!")
    record_data(n, begin, "Touchdown!")
    n += 1

        
    while ground_counter < 500:
        
        # Do transmission Here
        
        # Record Data Just in case
        record_data(n, begin, "Landed")
        n += 1
        time.sleep(sleep_time)
        ground_counter = ground_counter + 1
    
    os.exit(0)
   
 
		 
if __name__ == "__main__":
    main()
