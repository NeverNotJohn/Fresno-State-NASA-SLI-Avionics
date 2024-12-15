import serial
import json
import time
import board
import busio
import adafruit_bmp280

# Initialize I2C for BMP280
i2c = busio.I2C(board.SCL, board.SDA)
bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
bmp.sea_level_pressure = 1013.25  # Default sea level pressure in hPa

# Initialize UART for Reyax RYLR896
ser = serial.Serial('/dev/serial0', 115200, timeout=1)

def send_message(data):
    try:
        # Format the data as JSON
        message = json.dumps(data)
        
        # Send message via the LoRa module
        command = f"AT+SEND=0,{len(message)},{message}\r\n"
        ser.write(command.encode())
        time.sleep(0.001)  # Allow time for transmission
        
        # Read and print the module's response
        response = ser.readline().decode('utf-8').strip()
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error while sending data: {e}")

if __name__ == "__main__":
    print("Starting data transmission...")
    start_time = time.time()  # Record the start time
    try:
        while True:
            # Calculate elapsed time in seconds
            elapsed_time = round(time.time() - start_time, 2)

            # Collect data from BMP280
            data = {
                "t": elapsed_time,  # Elapsed time in seconds
                "tp": round(bmp.temperature, 2),
                "p": round(bmp.pressure, 2),
                "a": round(bmp.altitude, 2)
            }

            print(f"Send: {data}")
            send_message(data)

            time.sleep(.001)  # Send data every second
    except KeyboardInterrupt:
        print("Transmission stopped.")
    finally:
        ser.close()
