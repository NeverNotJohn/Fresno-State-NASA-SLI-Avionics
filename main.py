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
    
    bmp.calibrate_BMP280()
    GPS.calibrate_GPS()
    
    writer.writerow(["n", "timestamp (s)", "altitude (m)", "latitude", "longitude", "temperature", "pressure", "acceleration", "gyroscope", "battery"])

def record_data(n, begin):
    global writer
    
    altitude = bmp.read_altitude()
    temperature = bmp.read_temp()
    pressure = bmp.read_pressure()
    
    temp = GPS.get_GPS()
    latitude = temp[0]
    longitude = temp[1]
    
    # for Debug Reasons
    data = {
            "n": n, 
            "timestamp": time.time() - begin, 
            "altitude": altitude, 
            "latitude": latitude, 
            "longitude": longitude, 
            "temperature": temperature, 
            "pressure": pressure, 
            "acceleration": 0, 
            "gyroscope": 0, 
            "battery": 0
            }
    
    writer.writerow([n, time.time() - begin, altitude, latitude, longitude, temperature, pressure, 0, 0, 0])
    
    return data

def dic_to_string(data):
    string = ""
    for key, value in data.items():
        string += f"{key}: {value} "
    return string

#------------------------Main------------------------

def main():
    print("Hello World")
    initialize()
    
    n = 0
    begin = time.time()
    
    while True:
        
        data = record_data(n, begin)
        string = dic_to_string(data)
        
        print(string)
        n += 1
        time.sleep(0.1)
 
 
 
		 
if __name__ == "__main__":
    main()
