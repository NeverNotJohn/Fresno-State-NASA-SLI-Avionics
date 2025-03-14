""" Testing the berry """

import sys
import os

# Add subdir2 to path to access module2
sys.path.append(os.path.abspath("func"))

import time
import math
from func import berryIMU

print("Hello World")

berryIMU.read_imu_data()