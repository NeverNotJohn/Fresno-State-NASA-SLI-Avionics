import serial
import pynmea2

# Open serial port (adjust if using a different port)
serial_port = "/dev/serial0"  # UART on Raspberry Pi
baud_rate = 9600  # GPS6MV2 default

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    while True:
        line = ser.readline().decode('utf-8', errors='ignore')
        if line.startswith("$GPGGA") or line.startswith("$GPRMC"):
            try:
                msg = pynmea2.parse(line)
                print(f"Latitude: {msg.latitude}, Longitude: {msg.longitude}")
            except pynmea2.ParseError:
                continue
except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    ser.close()
