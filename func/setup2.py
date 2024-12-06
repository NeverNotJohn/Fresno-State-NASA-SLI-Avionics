import serial
import time

# Initialize the serial port (replace '/dev/serial0' if needed)
ser = serial.Serial('/dev/serial0', 115200, timeout=1)

def send_at_command(command):
    """
    Sends an AT command to the module and prints the response.
    """
    try:
        ser.write(f"{command}\r\n".encode())  # Send the command
        time.sleep(0.5)  # Wait for the response
        response = ser.readline().decode('utf-8', errors='ignore').strip()
        print(f"Command: {command} | Response: {response}")
    except Exception as e:
        print(f"Error sending command '{command}': {e}")

def configure_module():
    """
    Configures the Reyax RYLR896 module.
    """
    print("Starting module configuration...")
    
    send_at_command("AT")                   # Test communication
    send_at_command("AT+ADDRESS=2")         # Set address (adjust for each Pi, e.g., 2 for the second module)
    send_at_command("AT+NETWORKID=5")       # Set network ID (same for both modules)
    send_at_command("AT+BAND=915000000")    # Set frequency (adjust for your region)
    send_at_command("AT+IPR=15")            # Set RF power (optional)
    send_at_command("AT+PARAMETER")         # Confirm settings
    
    print("Configuration complete.")

if __name__ == "__main__":
    try:
        configure_module()
    finally:
        ser.close()
        print("Serial port closed.")
