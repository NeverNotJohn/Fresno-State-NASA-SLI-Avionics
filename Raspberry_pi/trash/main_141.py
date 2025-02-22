from func import bmp
import time
import csv
import datetime
import os
import sys
import RPi.GPIO as GPIO
import threading
from func.trash import heap_sort
from func.trash import Data_send
import csv
import serial

"""
Pins:

BMP280 -> PI4:
SCK -> 5
SDI -> 3

GPS6MV2 -> PI4:
TX -> 10
"""

#--------------------GPIO Setup--------------------
BUZZER_PIN = 6  # GPIO pin for the buzzer
GPIO.setwarnings(False)  # Disable GPIO warnings for a cleaner console output
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set GPIO 26 as input with pull-down resistor
GPIO.setup(BUZZER_PIN, GPIO.OUT)  # Set GPIO 6 as an output pin for the buzzer

#--------------------Global Variables--------------------
final_data = []  # Stores the final data recorded
begin = 0  # Start time of the project for timing calculations
annoy_cyan = True  # Controls whether the buzzer makes sounds
heap = heap_sort.MaxHeap("altitude")  # Initialize a max heap for altitude data

# Generate a unique filename based on the current timestamp
now = datetime.datetime.now().strftime("%c").replace(" ", "_").replace(":", ".")
filename = f"{os.path.dirname(__file__)}/data_141/{now}.csv"
print(filename)  # Debug: Print the filename to verify correctness

#--------------------Functions-----------------------

def write_csv(data, name):
    """
    Writes a list of dictionaries to a CSV file.
    Args:
        data: List of dictionaries containing data to write
        name: File name to save the CSV
    """
    keys = data[0].keys()  # Extract keys from the first dictionary
    with open(name, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()  # Write CSV header
        dict_writer.writerows(data)  # Write rows of data

def heap_thread(data):
    """
    Inserts data into the heap in a separate thread.
    Args:
        data: Dictionary containing the altitude data to insert
    """
    global heap
    heap.insert(data)

def beep(duration=0.2, times=3, pin=6):
    """
    Activates the buzzer for feedback.
    Args:
        duration: Time in seconds for each beep
        times: Number of beeps
        pin: GPIO pin for the buzzer
    """
    try:
        for i in range(times):
            GPIO.output(pin, GPIO.HIGH)  # Turn the buzzer on
            time.sleep(duration)  # Wait for the duration
            GPIO.output(pin, GPIO.LOW)  # Turn the buzzer off
            time.sleep(duration)  # Pause between beeps
    except Exception as e:
        print("Error: ", e)

def calibrate():
    """
    Calibrates the BMP280 sensor. Beeps when done.
    """
    bmp.calibrate_BMP280()  # Call the calibration function
    print("Calibrating Done!")
    if annoy_cyan:  # Beep if the annoyance feature is enabled
        beep()

def record():
    """
    Reads sensor data and formats it into a dictionary.
    Returns:
        Dictionary containing time, temperature, pressure, and altitude.
    """
    global begin
    altitude = bmp.read_altitude()  # Get altitude reading
    pressure = bmp.read_pressure()  # Get pressure reading
    temperature = bmp.read_temp()  # Get temperature reading
    
    data = {
        "time": round(time.time() - begin, 2),  # Time since start
        "temperature": round(temperature, 2),  # Rounded temperature
        "pressure": round(pressure, 2),  # Rounded pressure
        "altitude": round(altitude, 2)  # Rounded altitude
    }
    time.sleep(0.05)  # Small delay for sensor stability
    return data

def dic_to_string(data):
    """
    Converts a dictionary to a formatted string.
    Args:
        data: Dictionary to format
    Returns:
        Formatted string representation of the dictionary.
    """
    string = ""
    for key, value in data.items():
        string += f"{key}: {value}\n"
    return string

def button_press():
    """
    Waits for a button press to start the project, then calibrates the sensor.
    """
    beep(times=1)  # Single beep to signal ready state
    calibrate()  # Calibrate the sensor
    time.sleep(1)  # Wait for calibration to complete
    while True:
        if GPIO.input(26) == GPIO.HIGH:  # Detect button press
            project_start()

def project_start():
    """
    Initiates the project sequence upon button press.
    """
    print("Button Press")
    beep(times=1, duration=0.5)  # Short beep to confirm
    time.sleep(10)  # Initial delay for stabilization
    beep(times=4, duration=0.05)  # Signal the start
    time.sleep(0.1)
    beep(times=4, duration=0.05)  # Repeat beep sequence
    record_loop()  # Begin the data recording loop

def record_loop():
    """
    Main loop for recording sensor data and managing the heap.
    """
    global begin, final_data, now
    begin = time.time()  # Mark the start time
    n = 0  # Counter for consecutive low-altitude readings
    b = 0  # General iteration counter
    sort = True # Key for heapsort

    while n < 40:
        if annoy_cyan and (b % 10 == 0):  # Beep every 10 iterations if enabled
            beep(times=1, duration=0.05)
        
        data = record()  # Collect sensor data
        final_data.append(data)  # Append to the final data list
        
        altitude = data["altitude"]
        if altitude < 5:  # Check if altitude indicates ground level
            n += 1
        if altitude < 15 and sort:
            write_csv(heap.heapsort(10), f"{os.path.dirname(__file__)}/data_141/heapsort_{now}.csv")
            sort = False
        # Execute heap insertion in a separate thread
        heap_handler = threading.Thread(target=heap_thread, args=(data,))
        heap_handler.start()
        b += 1

    time.sleep(1)  # Short delay after recording completes

    if annoy_cyan:
        beep(times=2, duration=1)  # Signal the end of recording

    # Save recorded data and heap-related outputs to CSV files
    write_csv(final_data, filename)
    write_csv(heap.heap, f"{os.path.dirname(__file__)}/data_141/heap_{now}.csv")
    sys.exit()  # Exit the script

#------------------------Main------------------------

def main():
    """
    Main function for initializing and managing the project flow.
    """
    global annoy_cyan
    if not annoy_cyan:  # If annoyance is disabled, calibrate and start recording immediately
        calibrate()
        record_loop()
    
    print("Hello World")
    while True:  # Wait for a button press to start
        if GPIO.input(26) == GPIO.HIGH:
            button_press()

if __name__ == "__main__":
    main()

