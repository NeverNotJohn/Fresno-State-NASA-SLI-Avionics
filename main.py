from func import *
import time

def main():
    print("Hello World")
    
    n = 0
    begin = time.time()
    
    while True:
        
        data = {"n": n, "timestamp": time.time() - begin, "altitude": 0, "latitude": 0, "longitude": 0, "temperature": 0, "humidity": 0, "pressure": 0, "acceleration": 0, "gyroscope": 0, "battery": 0}
        print(data)
        n += 1
        time.sleep(0.1)
 
 
 
		 
if __name__ == "__main__":
    main()