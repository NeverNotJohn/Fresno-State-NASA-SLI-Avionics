import time
import board
import adafruit_bmp280

# Create sensor object, communicating over the board's default I2C bus
try:
    i2c = board.I2C()  # Initialize I2C communication using the board's default pins (SCL and SDA)
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)  # Connect to the BMP280 sensor at address 0x77
except Exception as e:
    print("Error: ", e)  # Handle initialization errors, e.g., if the sensor is not connected

#--------------------Functions--------------------

def calibrate_BMP280():
    """
    Calibrates the BMP280 sensor by calculating the average pressure over multiple readings
    and setting it as the sea level pressure for accurate altitude calculations.
    """
    global bmp280
    try:
        sum = 0
        n = 10  # Number of readings for calibration
        for i in range(n):
            sum += bmp280.pressure  # Accumulate pressure readings
            time.sleep(0.33)  # Wait briefly between readings to stabilize
        bmp280.sea_level_pressure = sum / n  # Set the calculated average as sea level pressure
    except Exception as e:
        print("Error during calibration: ", e)  # Handle any calibration errors

def read_temp():
    """
    Reads the temperature from the BMP280 sensor.
    Returns:
        Temperature in degrees Celsius, or -1 in case of an error.
    """
    global bmp280
    try:
        temp = bmp280.temperature  # Get temperature reading
    except Exception as e:
        print("Error: ", e)  # Handle reading errors
        temp = -1  # Return -1 to indicate an error
    return temp

def read_pressure():
    """
    Reads the pressure from the BMP280 sensor.
    Returns:
        Pressure in hPa, or -1 in case of an error.
    """
    global bmp280
    try:
        p = bmp280.pressure  # Get pressure reading
    except Exception as e:
        print("Error: ", e)  # Handle reading errors
        p = -1  # Return -1 to indicate an error
    return p

def read_altitude():
    """
    Reads the altitude from the BMP280 sensor, using the calibrated sea level pressure.
    Returns:
        Altitude in meters, or -1 in case of an error.
    """
    global bmp280
    try:
        alt = bmp280.altitude  # Get altitude reading
    except Exception as e:
        print("Error: ", e)  # Handle reading errors
        alt = -1  # Return -1 to indicate an error
    return alt

#--------------------Debugging Main Function--------------------
def main():
    """
    Debugging function to test BMP280 functionality. Continuously prints sensor readings
    (temperature, pressure, altitude) to the console.
    """
    print("Calibrating BMP280...")
    calibrate_BMP280()  # Perform initial calibration
    
    initial = time.time()  # Record the start time for relative timing
    while True:
        print("\nTime: %0.1f s" % (time.time() - initial))  # Print elapsed time
        print("Temperature: %0.1f C" % read_temp())  # Print temperature
        print("Pressure: %0.1f hPa" % read_pressure())  # Print pressure
        print("Altitude = %0.2f meters" % read_altitude())  # Print altitude
        time.sleep(3)  # Pause for 3 seconds between readings

# Entry point for the script
if __name__ == "__main__":
    main()

