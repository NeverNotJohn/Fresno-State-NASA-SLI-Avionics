import serial
import json
import time
import board
import busio
import adafruit_bmp280

# Initialize I2C for BMP280
i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
bmp.sea_level_pressure = 1013.25  # Adjust based on your location

# Initialize UART for Reyax RYLR896
ser = serial.Serial('/dev/serial0', 115200, timeout=1)

def send_message(data):
    try:
        # Format the data as JSON
        message = json.dumps(data)
        
        # Send message via the LoRa module
        command = f"AT+SEND=0,{len(message)},{message}\r\n"
        ser.write(command.encode())
        time.sleep(2)  # Allow time for transmission
        
        # Read and print the module's response
        response = ser.readline().decode('utf-8').strip()
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error while sending data: {e}")

if __name__ == "__main__":
    print("Starting data transmission...")

    try:
        while True:
            # Collect data from BMP280
            data = {
                "time": round(time.time(), 2),
                "temperature": round(bmp.temperature, 2),
                "pressure": round(bmp.pressure, 2),
                "altitude": round(bmp.altitude, 2)
            }

            print(f"Sending data: {data}")
            send_message(data)

            time.sleep(.001)  # Transmit every second
    except KeyboardInterrupt:
        print("Transmission stopped.")
    finally:
        # Ensure the port is closed when the script stops
        ser.close()
