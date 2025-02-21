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
LED     | GPIO18

BUZZER  | PI4:
PIN     | GPIO26

"""

"""--------------------CONSTANTS--------------------"""
# Constants that won't be touched

FLIGHT_MIN = 50
SLEEP_TIME = 0.5

"""--------------------GLOBAL VARS------------------"""
# Global Variables that will be used across functions

LAUNCHED = False
BEGIN_TIME = 0
n = 0










def main():
    print("Hello World")
    
if __name__ == "__main__":
    main()

