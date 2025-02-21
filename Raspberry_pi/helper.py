from func import bmp
from func import GPS6MV2
from func import MPU6050
from func import hv4pt
from func import GPS

import RPi.GPIO as GPIO
import time

"""--------------------CONSTANTS--------------------"""

# Data array Indexes
DATETIME = 0
EXECUTION_TIME = 1
ALTITUDE = 2
TEMPERATURE = 3
LONGITUDE = 4
LATITUDE = 5
ACC_X = 6
ACC_Y = 7
ACC_Z = 8

"""--------------------GPIO SETUP------=-----------"""

BUZZER_PIN = 26
FIREFLY_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

"""--------------------GLOBAL VARS------------------"""

APOGEE = 0
DATA_ARRAY = []


"""--------------------FUNCTIONS-----------------"""

def beep(pin=26, duration=0.2, times=3):
    """
    Beeps lol
    """
    
    
    try:
        for i in range(times):
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(duration)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(duration)
    except Exception as e:
        print("Error: ", e)
        
def dic_to_string(data):
    string = ""
    for key, value in data.items():
        string += f"{key}: {value}\n"
    return string
    
    
def calibrate():
    """
    Calibrates On-Board Sensors
    
    3 short Beeps = Finished Calibrating
    """
    global BUZZER_PIN
    
    print("Calibrating BMP280...")
    bmp.calibrate_BMP280()
    print("Calibrating MPU6050...")
    MPU6050.initialize_mpu6050()
    
    # Anything Else needs to calibrate?
    # FIXME
    
    print("Calibration Done!")
    beep(BUZZER_PIN)
    
def record_data(n, begin_time, writer, flag=""):
    """
    Records data to a CSV file and into array
    """
    global BUZZER_PIN
    global APOGEE
    global DATETIME, EXECUTION_TIME, ALTITUDE, TEMPERATURE, LONGITUDE, LATITUDE, ACC_X, ACC_Y, ACC_Z
    
    # Beep if it works
    if n % 5 == 0:
        beep(BUZZER_PIN, 0.2, 1)
        
    # Get Data
    altitude = round(bmp.read_altitude(),3)
    temperature = round(bmp.read_temp(),3)
    
    temp = GPS.get_GPS()
    latitude = temp[0]
    longitude = temp[1]
    
    latitude = 0 # FIXME
    longitude = 0 # FIXME
    
    # FIXME
    acc = MPU6050.get_sensor_data()[0]
    acc_x = acc["x"]
    acc_y = acc["y"]
    acc_z = acc["z"]
    
    data = {
            "n": n,
            "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": round(time.time() - begin_time,3),
            "altitude": altitude,
            "temperature": temperature,
            "longitude": longitude,
            "latitude": latitude,
            "acc_x": acc_x,
            "acc_y": acc_y,
            "acc_z": acc_z
            }
    
    # Debug
    
    return data
    
def main():
    # Test Main
    
    # Initialize Sensors
    calibrate()
    
    # Testing function
    n=0
    begin_time = time.time()
    while True:
        print(dic_to_string(record_data(n, begin_time, None)))
        n+=1
        time.sleep(1)
        
if __name__ == "__main__":
    main()
    