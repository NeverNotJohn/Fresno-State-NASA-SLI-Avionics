import serial

ser = serial.Serial('/dev/serial0', 115200, timeout=1)

ser.write(b'AT\r\n')
response = ser.readline()
print(f"Raw Response: {response}")  # Print raw response for debugging

decoded_response = response.decode('utf-8').strip()
print(f"Decoded Response: {decoded_response}")

ser.close()
