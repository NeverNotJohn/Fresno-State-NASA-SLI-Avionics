from machine import Pin
import bmp
import GPS
import time

"""

File For general helper functions

"""
def beep(buzzer, duration=0.2, times=3):
    try:
        for i in range(times):
            buzzer.value(1)
            time.sleep(duration)
            buzzer.value(0)
            time.sleep(duration)
    except Exception as e:
        print("Error: ", e)
        
def initialize():
    print("Calibrating..")
    
def dic_to_string(data):
    string = ""
    for key, value in data.items():
        string += f"{key}: {value}\n"
    return string

def record_data(n, begin, buzzer_pin, global_data, flag="",):
    global writer
    
    # Beep if it works
    if n % 5 == 0:
        beep(buzzer_pin, 0.2, 1)
    
    altitude = round(bmp.read_altitude(),3)
    temperature = round(bmp.read_temp(),3)
    pressure = round(bmp.read_pressure(), 3)
    
    temp = GPS.get_GPS()
    latitude = temp[0]
    longitude = temp[1]
    
    # for Debug Reasons
    data = {
            "n": n, 
            "timestamp": (time.ticks_diff(time.ticks_ms(), begin)) / 1000, 
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
    
    #writer.writerow([n, round(time.time() - begin,3), altitude, latitude, longitude, temperature, pressure, 0, 0, 0, flag])
    global_data.append(data)
    string = dic_to_string(data)
    print(string, "\n")
    
    return data

def main():
    while True:
        print(time.ticks_us())
        time.sleep(1)

if __name__ == "__main__":
    main()