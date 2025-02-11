import bmp
import helper
from server import ap_mode
from machine import Pin
import _thread
import time
import server


"""
Pin Layout for Raspberry Pi Pico W:

    +----------------------------------------+
    GP0  [ 1] |  o o  | [40] VBUS            |
    GP1  [ 2] |       | [39] VSYS            |
    GND  [ 3] |       | [38] GND             |
    GP2  [ 4] |       | [37] 3V3_EN          |
    GP3  [ 5] |       | [36] 3V3             |
    GP4  [ 6] |       | [35] ADC_VREF        |
    GP5  [ 7] |       | [34] GP28 (ADC2)     |
    GND  [ 8] |       | [33] GND             |
    GP6  [ 9] |       | [32] GP27 (ADC1)     |
    GP7  [10] |       | [31] GP26 (ADC0)     |
    GP8  [11] |       | [30] RUN             |
    GP9  [12] |       | [29] GP22            |
    GND  [13] |       | [28] GND             |
    GP10 [14] |       | [27] GP21            |
    GP11 [15] |       | [26] GP20            |
    GP12 [16] |       | [25] GP19 (I2C SCL1) |
    GP13 [17] |       | [24] GP18 (SPI RX)   |
    GND  [18] |       | [23] GND             |
    GP14 [19] |       | [22] GP17 (SPI CLK)  |
    GP15 [20] |       | [21] GP16 (SPI TX)   |
    +----------------------------------------+

"""

"""
Our Pins

    +----------------------------------------+
         [ 1] |  o o  | [40] VBUS            |
    GP1  [ 2] |       | [39] VSYS            |
    GND  [ 3] |       | [38] GND             |
    GP2  [ 4] |       | [37] 3V3_EN          |
    GP3  [ 5] |       | [36] 3V3             |
    GP4  [ 6] |       | [35] ADC_VREF        |
    GP5  [ 7] |       | [34] GP28 (ADC2)     |
    GND  [ 8] |       | [33] GND             |
    GP6  [ 9] |       | [32] GP27 (ADC1)     |
    GP7  [10] |       | [31] GP26 (ADC0)     |
    GP8  [11] |       | [30] RUN             |
    GP9  [12] |       | [29] GP22            |
    GND  [13] |       | [28] GND             |
    GP10 [14] |       | [27] GP21            |
    GP11 [15] |       | [26] GP20            |
    GP12 [16] |       | [25] GP19 (I2C SCL1) |
    GP13 [17] |       | [24] GP18 (SPI RX)   |
    GND  [18] |       | [23] GND             |
    GP14 [19] |       | [22] GP17 (SPI CLK)  |
    GP15 [20] |       | [21] GP16 (SPI TX)   |
    +----------------------------------------+

"""

"""-------------------Globals----------------------"""
data = "data"

# Objects
bmp_object = bmp.BMP280()

"""-------------------GPIO Setup-------------------"""
led = Pin("LED", Pin.OUT)
buzzer = Pin(15, Pin.OUT)

"""-------------------Main Code-------------------"""

def main():
    
    print("starting!")
    """ Debug """
    
    # Define the pin for the LED
    # Define threads

    #_thread.start_new_thread(helper.record_data, ())

    # Turned On!
    helper.beep(buzzer, 0.5, 3)
    
    """ Variables """
    launched = False
    landed = False
    flight_min = 50
    sleep_time = 0.5
    
    """ Calibrating """
    # FIXME calibrate Have WIFI Button
    helper.initialize()
    bmp_object.calibrate()
    
    
    
    """ Before Launch """
    # FIXME Press Button to Start Recording
    
    # Launch Variables
    n = 0
    begin = time.ticks_ms()
    altitude = 0
    
    while altitude < flight_min:
        altitude = (helper.record_data(n, begin, buzzer_pin=buzzer, global_data=data, bmp=bmp_object))["altitude"]
        n += 1
        time.sleep(sleep_time)
    
    # Launch Detected
    print("Launch Detected")
    launched = True
    helper.record_data(n, begin, "Launch Detected", data, bmp=bmp_object)
    
    
    
    """ During Launch """
    ground_counter = 0
    
    while ground_counter < 50:
        altitude = (helper.record_data(n, begin, buzzer_pin=buzzer, global_data=data, bmp=bmp_object))["altitude"]
        n += 1
        time.sleep(sleep_time)
        
        if (altitude < flight_min):
            ground_counter += 1
            
            
            
    """ Landed """
    print("Touchdown!")
    landed = True
    helper.record_data(n, begin, "Touchdown!", global_data=data, bmp=bmp_object)
    n += 1
    
    while ground_counter < 500:
        
        # Do Transmission Here
        
        time.sleep(sleep_time)
        ground_counter += 1
    
        
if __name__ == "__main__":
    led.value(1)
    #_thread.start_new_thread(ap_mode, ('john_pico', 'PASSWORD', data))
    main()
    