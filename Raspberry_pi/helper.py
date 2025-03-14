from func import bmp
from func import GPS6MV2
from trash import MPU6050
from func import kv4pt

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
MAX_VELOCITY = 0


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
    
def calculate_velocity(prev_altitude, curr_altitude, prev_time, curr_time):
    """
    Calculates velocity based on altitude change over time.
    
    Args:
        prev_altitude (float): Previous altitude reading.
        curr_altitude (float): Current altitude reading.
        prev_time (float): Previous timestamp.
        curr_time (float): Current timestamp.

    Returns:
        float: Velocity in m/s, or None if calculation fails.
    """
    try:
        if prev_time is None or prev_altitude is None:
            return None  # First reading, velocity cannot be determined
        
        if curr_time - prev_time == 0:
            return None  # Prevent division by zero

        velocity = (curr_altitude - prev_altitude) / (curr_time - prev_time)
        return round(velocity, 3)
    except Exception as e:
        print("Error calculating velocity:", e)
        return None    

def record_data(n, begin_time, flag=""):
    """
    Records data to a CSV file and into array
    """
    global BUZZER_PIN
    global APOGEE
    global DATETIME, EXECUTION_TIME, ALTITUDE, TEMPERATURE, LONGITUDE, LATITUDE, ACC_X, ACC_Y, ACC_Z, MAX_VELOCITY
    
    # Beep if it works
    if n % 5 == 0:
        beep(BUZZER_PIN, 0.2, 1)
        
    # Get Previous Data
    prev_altitude = DATA_ARRAY[-1]["altitude"] if DATA_ARRAY else None
    prev_time = DATA_ARRAY[-1]["timestamp"] if DATA_ARRAY else None        

    # Get Data
    # Get altitude/velocity
    try:
        curr_time = round(time.time() - begin_time, 3)
        altitude = round(bmp.read_altitude(), 3)
        velocity = calculate_velocity(prev_altitude, altitude, prev_time, curr_time)
    except Exception as e:
        print("Error reading altitude data: ", e)
        altitude = None
        velocity = None
        
    # Update max velocity
    if velocity is not None:
        MAX_VELOCITY = max(MAX_VELOCITY, velocity)
    
    # Get Temperature
    try:
        temperature = round(bmp.read_temp(), 3)
    except Exception as e:
        print("Error reading temperature data: ", e)
        temperature = None
    
    # Get GPS Data
    try:
        temp = GPS6MV2.get_GPS()
        latitude = temp[0]
        longitude = temp[1]
    except Exception as e:
        print("Error reading GPS data: ", e)
        latitude = longitude = None
        
    # Convert from m to ft and m/s to ft/s
    altitude = altitude * 3.28084 if altitude is not None else None
    velocity = velocity * 3.28084 if velocity is not None else None
    
    data = {
            "n": n,
            "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": round(time.time() - begin_time,3),
            "altitude": altitude,
            "velocity": velocity,
            "temperature": temperature,
            "longitude": longitude,
            "latitude": latitude,
            "angle_x": -1,
            "angle_y": -1,
            "flag": flag
            }
    
    # Add Data to data array
    DATA_ARRAY.append(data)
    
    # Debug
    print(dic_to_string(data))
    
    
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
    
