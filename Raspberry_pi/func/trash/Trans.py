import time
import board
import busio
import digitalio
import adafruit_rfm9x

# Define the pins based on the wiring guide
CS = digitalio.DigitalInOut(board.CE1)     # CE1 (GPIO7) for CS
RESET = digitalio.DigitalInOut(board.D25)  # GPIO25 for RESET

# Initialize SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize RFM9x module
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)  # Adjust frequency if needed
rfm9x.tx_power = 13

# Send a message
print("Sending test message...")
rfm9x.send("Loopback test message".encode('utf-8'))

# Immediately check for the message
print("Waiting for response...")
time.sleep(1)
packet = rfm9x.receive(timeout=2.0)
if packet is not None:
    print("Received:", packet.decode('utf-8'))
else:
    print("No response received.")