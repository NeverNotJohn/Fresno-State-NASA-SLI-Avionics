from func import bmp
import time
import csv
import datetime
import os
import sys
import RPi.GPIO as GPIO
import threading
from func import heap_sort
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

#--------------------GPIO Setuppp--------------------
BUZZER_PIN = 6										# GPIO 6
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)


#--------------------Globals Vars--------------------
final_data = []
begin = 0
annoy_cyan = True
heap = heap_sort.MaxHeap("altitude")

now = datetime.datetime.now().strftime("%c")
now = now.replace(" ", "_")
now = now.replace(":", ".")
filename = f"{os.path.dirname(__file__)}/data_141/{now}.csv"
print(filename)

#--------------------Functions-----------------------

def write_csv(data, name):
	keys = data[0].keys()
	
	with open(name, 'w', newline='') as output_file:
		dict_writer = csv.DictWriter(output_file,keys)
		dict_writer.writeheader()
		dict_writer.writerows(data)

def heap_thread(data):
	global heap
	heap.insert(data)
	

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
	if (annoy_cyan):
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
	global final_data
	global now 
	
	begin = time.time()
	n = 0
	b = 0
	while n < 40:
		
		if (annoy_cyan and (b % 10 == 0)):
			beep(times=1, duration=0.05)
		
		data = record()
		final_data.append(data)
		altitude = data["altitude"]
		print(dic_to_string(data))
		if (altitude < 5):	# Detect on ground with some leeway
			n = n + 1
		
		# Execute Heap Thread
		heap_handler = threading.Thread(target=heap_thread, args=(data,))
		heap_handler.start()
		
		b = b + 1
		
		
	
	time.sleep(1)
	
	if (annoy_cyan):
		beep(times=2, duration=1)
	
	# Stop
	
	m = 10
	#print(f"Heap = {heap}")
	#print(f"Data = {final_data}")
	#print(f"Heap Sorted {m} values:\n", heap.heapsort(m))  
	write_csv(final_data, filename)
	write_csv(heap.heap, (f"{os.path.dirname(__file__)}/data_141/heap_{now}.csv"))
	write_csv(heap.heapsort(m), (f"{os.path.dirname(__file__)}/data_141/heapsort_{now}.csv"))
	
	
	
	
	

	

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
	
if __name__ == "__main__":
    main()

