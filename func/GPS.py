import serial
import time
import string
import pynmea2

def calibrate_GPS():
	
	global poty, ser, dataout, newdata
	
	port="/dev/ttyS0"
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	newdata=ser.readline()

def get_GPS():
	# x[0] = lat
	# x[1] = lng
	newmsg=pynmea2.parse(newdata.decode("utf-8"))
	lat=newmsg.latitude
	lng=newmsg.longitude
	return [lat,lng]


""" Main function for debugging """
		
def main():
	calibrate_GPS()
	while True:
		gps_data = get_GPS()
		gps = "Latitude=  " + str(gps_data[0])+ "  and Longitude=" + str(gps_data[1])
		print(gps)
		time.sleep(1)
		 
if __name__ == "__main__":
    main()