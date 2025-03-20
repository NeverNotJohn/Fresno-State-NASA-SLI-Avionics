import serial
import time
import string
import pynmea2
import threading

"""-----GLOBALS-----"""

global_lat = -1
global_lng = -1
GPS_lock = threading.Lock()


"""-----FUNCTIONS-----"""

def get_GPS():
	# x[0] = lat
	# x[1] = lng
 
	global global_lat, global_lng, GPS_lock
 
	while True:
 
		try:
			port = "/dev/serial0"
			ser = serial.Serial(port, baudrate=9600, timeout=0)
			newdata = ser.readline()
			newmsg = pynmea2.parse(newdata.decode("utf-8"))
			lat = newmsg.latitude
			lng = newmsg.longitude
   
			# Debug
			print("Latitude: ", lat)
			print("Longitude: ", lng)
	
			# Update global variables
			with GPS_lock:
				global_lat = lat
				global_lng = lng
	
			ser.close
		except Exception as e:
			#print("GPS ERROR")
			lat = -1
			lng = -1


""" Main function for debugging """
		
def main():
	get_GPS()
 
		 
if __name__ == "__main__":
    main()
