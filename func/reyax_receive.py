import serial

# Initialize the serial port
ser = serial.Serial('/dev/serial0', 115200, timeout=1)

def receive_message():
    try:
        while True:
            # Read incoming data from the LoRa module
            response = ser.readline().decode('utf-8').strip()
            if response:
                print(f"Received: {response}")
    except KeyboardInterrupt:
        print("Stopped receiving.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    print("Listening for messages...")
    receive_message()
