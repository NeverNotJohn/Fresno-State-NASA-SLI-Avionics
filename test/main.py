import machine
import time

led = machine.Pin("LED", machine.Pin.OUT)  # Changed GPIO pin to 1

while True:
    led.value(1)
    print("LED is ON")
    time.sleep(1)  # Sleep for 1 second

    led.value(0)
    print("LED is OFF")
    time.sleep(1)  # Sleep for 1 second