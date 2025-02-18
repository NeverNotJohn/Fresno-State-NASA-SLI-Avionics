import serial
import time



PORT = 'COM3'
BAUD_RATE = 230400

ser = serial.Serial(PORT, BAUD_RATE, bytesize=serial.EIGHTBITS, 
                        parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, 
                        xonxoff=False, rtscts=False, dsrdtr=False)

# Give some time to establish the connection
time.sleep(2)
# DE AD BE EF DE AD BE EF
# DE AD BE EF DE AD BE EF 06 76
try:
    # Send data
    #send_data = b'\x41\x41\x41'
    #print(send_data)
    #ser.write(send_data)  # Convert string to bytes and send
    #print("Sent!")

    # Read response (if any)
    while True:
        time.sleep(0.1)
        received_data = ser.readline() 
        if received_data:
            print(received_data)
        else:
            print("No response received.")

except Exception as e:
    print("Error:", e)

finally:
    # Close the serial port
    ser.close()
    
    
"""

This sends raw data
No added append stuff

"""
