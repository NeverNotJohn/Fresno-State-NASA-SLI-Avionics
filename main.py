from func import bmp
from func import GPS
import time
import csv

"""
Pins:

BMP280 -> PI4:
SCK -> 5
SDI -> 3

GPS6MV2 -> PI4:
TX -> 10

"""

#--------------------Globals Vars--------------------
filename = "data.csv"
writer = csv.writer(open(filename, "w", newline=""))


#--------------------Functions-----------------------
def initialize():
    global writer
    
    print("Calibrating..")
    bmp.calibrate_BMP280()
    print("Calibrating...")
    GPS.calibrate_GPS()
    print("Calibrating Done!")
    
    writer.writerow(["n", "timestamp (s)", "altitude (m)", "latitude", "longitude", "temperature (C)", "pressure (hPa)", "acceleration", "gyroscope", "battery", "Flags"])

def dic_to_string(data):
    string = ""
    for key, value in data.items():
        string += f"{key}: {value} "
    return string

def record_data(n, begin, flag=""):
    global writer
    
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
    print(string)
    
    return data

#------------------------Main------------------------

def main():
	
    print("Calibrating.")
    initialize()
    
    # Variables
    n = 0
    begin = time.time()
    launched = False
    landed = False
    
    # Before Launch
    altitude = 0
    while altitude < 50:                                            # 50 meters  
        altitude = bmp.bmp280.altitude
        record_data(n, begin)
        n += 1
        time.sleep(0.5)
    
    # Set Launch Bit to True and record on .csv
    launched = True
    print("Launch Detected")
    record_data(n, begin, "Launch Detected")
    
    # During Launch
    ground_counter = 0		                                        # Counts how many points below 50m
    
    while ground_counter < 50:                                      # About 25 seconds
        altitude = bmp.bmp280.altitude
        record_data(n, begin)
        n += 1
        time.sleep(0.5)
		
        if (altitude < 50):                                         # 50 meters
            ground_counter = ground_counter + 1
			
	# Landed
    landed = True
    print("Touchdown!")
    record_data(n, begin, "Touchdown!")
    n += 1

        
    while True:
        
        # Do transmission Here
        
        # Record Data Just in case
        record_data(n, begin, "Landed")
        n += 1
        time.sleep(0.5)
   
 
		 
if __name__ == "__main__":
    main()
