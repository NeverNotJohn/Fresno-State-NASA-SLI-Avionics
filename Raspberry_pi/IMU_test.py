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
    
    global global_kalman_x, global_kalman_y
    global berry_stop, berry_lock

    print("Hello World")


    berry_thread = threading.Thread(target=berryIMU.read_imu_data)
    berry_thread.start()

    for _ in range(5):

        with berry_lock:
            print(f"x: {global_kalman_x}, y: {global_kalman_y}")
            time.sleep(3)
            
    with berry_lock:
        berry_stop = True
        print("Stopping BerryIMU thread")

if __name__ == "__main__":
    main()