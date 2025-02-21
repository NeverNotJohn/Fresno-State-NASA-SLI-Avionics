from func import bmp
from func import MPU6050
from func import hv4pt

import time
import csv
import datetime
import os
import RPi.GPIO as GPIO

"""
--------------------PIN LAYOUT--------------------
USING PIN NAME

BMP280  | PI4:
SCK     | SCL1
SDI     | SDA1

MPU6050 | PI4:
SCL     | SCL1
SDA     | SDA1

GPS6MV2 | PI4:
RX      | TXD0
TX      | RXD0

HV4PT   | PI4:
USB     | TOP BLUE USB PORT

FIREFLY | PI4:
LED     | ???

BUZZER  | PI4:
PIN     | GPIO26

"""

"""--------------------Constants--------------------"""
# Constants that won't be touched

FLIGHT_MIN = 50
SLEEP_TIME = 0.5

"""--------------------Globals Vars-----------------"""
# Global Variables that will be used across functions

LAUNCHED = False
BEGIN_TIME = 0
n = 0


"""--------------------GPIO Setuppp-----------------"""

BUZZER_PIN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)







def main():
    print("Hello World")
    
if __name__ == "__main__":
    main()

