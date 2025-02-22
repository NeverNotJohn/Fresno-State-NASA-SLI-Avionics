import smbus
import time

# MPU6050 I2C Address
MPU6050_ADDR = 0x68

# MPU6050 Register Addresses
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# MPU6050 Sensitivity Scale Factors
ACCEL_SCALE = 16384.0  # 1g = 16384 LSB (±2g range)
GYRO_SCALE = 131.0     # 1°/s = 131 LSB (±250°/s range)

# Initialize I2C bus (Use 0 for GPIO0 & GPIO1, or 1 for GPIO2 & GPIO3)
I2C_BUS = 1  # Change to 1 if using standard I2C pins
bus = smbus.SMBus(I2C_BUS)

def initialize_mpu6050():
    try:
        """ Wakes up the MPU6050 from sleep mode """
        bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)
        time.sleep(0.1)  # Give the sensor time to wake up
    except Exception as e:
        print(f"Error initializing MPU6050: {e}")

def read_word(register):
    """ Reads two bytes from the given register and combines them into a signed 16-bit value """
    high = bus.read_byte_data(MPU6050_ADDR, register)
    low = bus.read_byte_data(MPU6050_ADDR, register + 1)
    value = (high << 8) | low  # Combine high and low bytes
    
    # Convert to signed value
    if value >= 0x8000:
        value -= 65536  # Convert to negative
    
    return value

def get_sensor_data():
    """ Reads acceleration and gyroscope data from MPU6050 and converts them to real-world units """
    try:
        accel = {
            "x": read_word(ACCEL_XOUT_H) / ACCEL_SCALE,  # Convert to g
            "y": read_word(ACCEL_XOUT_H + 2) / ACCEL_SCALE,
            "z": read_word(ACCEL_XOUT_H + 4) / ACCEL_SCALE
        }
        gyro = {
            "x": read_word(GYRO_XOUT_H) / GYRO_SCALE,  # Convert to °/s
            "y": read_word(GYRO_XOUT_H + 2) / GYRO_SCALE,
            "z": read_word(GYRO_XOUT_H + 4) / GYRO_SCALE
        }
        return accel, gyro
    except Exception as e:
        print(f"Error reading sensor data: {e}")
        return None, None

def main():
    """ Main loop to read and display MPU6050 data with units """
    initialize_mpu6050()
    
    try:
        while True:
            accel, gyro = get_sensor_data()
            print(f"Accel (g): X={accel['x']:.2f}, Y={accel['y']:.2f}, Z={accel['z']:.2f} | "
                  f"Gyro (°/s): X={gyro['x']:.2f}, Y={gyro['y']:.2f}, Z={gyro['z']:.2f}")
            time.sleep(1)  # Read every second
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()

