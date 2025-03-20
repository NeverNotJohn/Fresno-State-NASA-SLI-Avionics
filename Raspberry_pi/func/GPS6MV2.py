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
			ser = serial.Serial(port, baudrate=9600, timeout=0.5)
			newdata = ser.readline()
			newmsg = pynmea2.parse(newdata.decode("utf-8"))
			lat = newmsg.latitude
			lng = newmsg.longitude
	
			# Update global variables
			with GPS_lock:
				global_lat = lat
				global_lng = lng
	
			ser.close
		except Exception as e:
			print("GPS ERROR")
			lat = -1
			lng = -1


""" Main function for debugging """
		
def main():
	while True:
		gps_data = get_GPS()
		gps = "Latitude=  " + str(gps_data[0])+ "  and Longitude=" + str(gps_data[1])
		print(gps)
		time.sleep(1)
		 
if __name__ == "__main__":
    main()
