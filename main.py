from func import *
import time
import csv

#--------------------Globals Vars--------------------
filename = "data.csv"
writer = csv.writer(open(filename, "w", newline=""))


#--------------------Functions-----------------------
def initialize():
    global writer
    writer.writerow(["n", "timestamp", "altitude", "latitude", "longitude", "temperature", "pressure", "acceleration", "gyroscope", "battery"])

def record_data(n, begin):
    global writer
    
    # for Debug Reasons
    data = {
            "n": n, 
            "timestamp": time.time() - begin, 
            "altitude": 0, 
            "latitude": 0, 
            "longitude": 0, 
            "temperature": 0, 
            "pressure": 0, 
            "acceleration": 0, 
            "gyroscope": 0, 
            "battery": 0
            }
    
    writer.writerow([n, time.time() - begin, 0, 0, 0, 0, 0, 0, 0, 0])
    
    return data

def dic_to_string(data):
    string = ""
    for key, value in data.items():
        string += f"{key}: {value} "
    return string

#------------------------Main------------------------

def main():
    print("Hello World")
    initialize()
    
    n = 0
    begin = time.time()
    
    while True:
        
        data = record_data(n, begin)
        string = dic_to_string(data)
        
        print(string)
        n += 1
        time.sleep(0.1)
 
 
 
		 
if __name__ == "__main__":
    main()