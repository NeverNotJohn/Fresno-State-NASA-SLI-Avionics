""" Testing the berry """

import sys
import os

# Add subdir2 to path to access module2
sys.path.append(os.path.abspath("func"))

import time
import math
from func import berryIMU
import threading

def main():

    print("Hello World")


    berry_thread = threading.Thread(target=berryIMU.read_imu_data)
    berry_thread.start()

    for _ in range(5):

        with berryIMU.berry_lock:
            print(f"x: {berryIMU.global_kalman_x}, y: {berryIMU.global_kalman_y}")

        time.sleep(3)
            
    with berryIMU.berry_lock:
        berryIMU.berry_stop = True
        print("Stopping BerryIMU thread")
        
    time.sleep(10)

if __name__ == "__main__":
    main()