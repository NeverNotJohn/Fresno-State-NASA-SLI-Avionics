from func import bmp
import time
import csv
import datetime
import os
import sys
import RPi.GPIO as GPIO
import threading

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
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)


#--------------------Globals Vars--------------------
begin = 0
annoy_cyan = False

#--------------------Functions-----------------------

def beep(duration=0.2, times=3, pin=6):
	try:
		for i in range(times):
			GPIO.output(pin, GPIO.HIGH)
			time.sleep(duration)
			GPIO.output(pin, GPIO.LOW)
			time.sleep(duration)
	except Exception as e:
		print("Error: ", e)
	

def calibrate():
	bmp.calibrate_BMP280()
	print("Calibrating Done!")
	beep()

def record():
	global begin
	
	altitude = bmp.read_altitude()
	pressure = bmp.read_pressure()
	temperature = bmp.read_temp()
	
	data = {
		"time": round(time.time() - begin, 2),
		"temperature" : round(temperature, 2),
		"pressure" : round(pressure, 2),
		"altitude" : round(altitude, 2)
	}
	time.sleep(0.1)
	return data

def dic_to_string(data):
    string = ""
    for key, value in data.items():
        string += f"{key}: {value}\n"
    return string

def button_press():
	# Wait till button press
	beep(times=1)
	calibrate()
	time.sleep(1)
	while True:
		if GPIO.input(26) == GPIO.HIGH:
			project_start()
		time.sleep(0.1)

def project_start():
	print("Button Press")
	beep(times=1, duration = 0.5)
	
	# Project start
	time.sleep(10)
	beep(times=4, duration=0.05)
	time.sleep(0.1)
	beep(times=4, duration=0.05)
	
	record_loop()

def record_loop():
	global begin
	begin = time.time()
	n = 0
	while n < 20:
		data = record()
		altitude = data["altitude"]
		print(dic_to_string(data))
		if (altitude < 5):	# Detect on ground with some leeway
			n = n + 1
	

#--------------------Interrupts----------------------
#GPIO.add_event_detect(26,GPIO.RISING,callback=button_press) # Setup event on pin 10 rising edge

#------------------------Main------------------------

def main():
	global annoy_cyan
	if (not annoy_cyan):
		calibrate()
		record_loop()
	
	print("Hello World")
	
	# Wait till button press
	while True:
		if GPIO.input(26) == GPIO.HIGH:
			button_press()
		time.sleep(0.1)
	
if __name__ == "__main__":
    main()

