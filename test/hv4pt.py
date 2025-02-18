import serial
import time
import threading

"""-------------------------TODO------------------------------"""
"""
    - Send issue to github
    - Join discord and discuss issue
"""

"""-------------------------CONSTANTS-------------------------"""

PORT = 'COM3'
BAUD_RATE = 230400      # 230400 bits per second
DATA_BITS = 8
PARITY = 'N'
STOP_BITS = 1
FLOW_CONTROL = None

"""-------------------------COMMANDS--------------------------"""

DELIMITER = b'\xFF\x00\xFF\x00\xFF\x00\xFF\x00'
COMMAND_PTT_DOWN = b'\xFF\x00\xFF\x00\xFF\x00\xFF\x00\x01'
COMMAND_PTT_UP = b'\xFF\x00\xFF\x00\xFF\x00\xFF\x00\x02'
COMMAND_TUNE_TO = b'\xFF\x00\xFF\x00\xFF\x00\xFF\x00\x03\x31\x34\x34\x2E\x33\x39\x30\x30\x31\x34\x34\x2E\x33\x39\x30\x30\x00\x00\x06\x57'
"""
// Delimiter               C  Parameters
FF 00 FF 00 FF 00 FF 00 03 31 34 34 2E 33 39 30 30 31 34 34 2E 33 39 30 30 00 00 06 57
                           Transmit freq           Receive freq            Tone  Sq Bandwidth
                           144.3900                144.3900                0     6  W
"""

"""-------------------------FUNCTIONS-------------------------"""

def send_serial_data(data, port, baud_rate):
    try:
        ser = serial.Serial(port, baud_rate, bytesize=serial.EIGHTBITS, 
                        parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, 
                        xonxoff=False, rtscts=False, dsrdtr=False)
        ser.write(data)
        ser.close()
    except serial.SerialException as e:
        print(f"Error: {e}")
        
def send_wav_over_serial(wav_file_path, port='COM3', baud_rate=230400, chunk_size=532288):
    """
    Sends a .wav file over a serial connection.

    :param wav_file_path: Path to the .wav file.
    :param serial_port: Serial port to send data to (e.g., "COM3" or "/dev/ttyUSB0").
    :param baud_rate: Baud rate for the serial connection.
    :param chunk_size: Size of each data chunk to send.
    """
    try:
        # Open the serial connection
        with serial.Serial(port, baud_rate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, xonxoff=False, rtscts=False, dsrdtr=False) as ser, open(wav_file_path, "rb") as wav_file:
            while chunk := wav_file.read(chunk_size):
                ser.write(chunk)  # Send over serial
                #print(chunk)
                print(f"Sent {len(chunk)} bytes")

        print("File transmission complete.")

    except Exception as e:
        print(f"Error: {e}")
        
        
"""-------------------------MAIN-------------------------"""

def main():
    print("Begin!")
    time.sleep(2)
    send_serial_data(COMMAND_TUNE_TO, PORT, BAUD_RATE)
    print("Tuning to 144.3900")
    time.sleep(3)
    send_serial_data(COMMAND_PTT_DOWN, PORT, BAUD_RATE)
    print("PTT Down")
    time.sleep(3)
    print("Sending audio...")
    send_wav_over_serial("8b.wav", PORT, BAUD_RATE)
    time.sleep(1)
    send_serial_data(COMMAND_PTT_UP, PORT, BAUD_RATE)
    print("PTT Up")
    

if __name__ == "__main__":
    main()