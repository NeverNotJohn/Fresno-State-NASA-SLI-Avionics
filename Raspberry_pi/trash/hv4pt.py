import serial
import time
import threading
from pydub import AudioSegment

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
COMMAND_TUNE_TO = b'\xFF\x00\xFF\x00\xFF\x00\xFF\x00\x03\x31\x34\x36\x2E\x35\x32\x30\x30\x31\x34\x36\x2E\x35\x32\x30\x30\x00\x00\x06\x57'
"""
// Delimiter               C  Parameters
FF 00 FF 00 FF 00 FF 00 03 31 34 36 2E 35 32 30 30 31 34 36 2E 35 32 30 30 00 00 06 57
                           Transmit freq           Receive freq            Tone  Sq Bandwidth
                           146.5200                146.5200                0     6  W
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
    
    
    
def combine_wav_files(input_files, output_file):
    combined = AudioSegment.empty()
    
    for file in input_files:
        sound = AudioSegment.from_wav(file)
        combined += sound  # Concatenating audio files
    
    combined.export(output_file, format="wav")
    print(f"Combined file saved as {output_file}")
        
"""-------------------------MAIN-------------------------"""

def main():
    print("Begin!")
    time.sleep(5)
    send_serial_data(COMMAND_TUNE_TO, PORT, BAUD_RATE)
    print("Tuning to 144.3900")
    time.sleep(1)
    send_serial_data(COMMAND_PTT_DOWN, PORT, BAUD_RATE)
    time.sleep(1)
    send_serial_data(COMMAND_PTT_DOWN, PORT, BAUD_RATE)
    time.sleep(1)
    send_serial_data(COMMAND_PTT_DOWN, PORT, BAUD_RATE)
    time.sleep(1)
    print("PTT Down")
    time.sleep(1.5)
    print("Sending audio...")
    
    example = ["audio/call_sign.wav","audio/temperature.wav", "audio/2.wav", "audio/3.wav", "audio/point.wav", "audio/5.wav", "audio/6.wav", "audio/celcius.wav", "audio/call_sign.wav"]
    combine_wav_files(example, "audio/combined.wav")
    send_wav_over_serial("audio/combined.wav", PORT, BAUD_RATE)
    
    time.sleep(1)
    send_serial_data(COMMAND_PTT_UP, PORT, BAUD_RATE)
    print("PTT Up")
    

if __name__ == "__main__":
    main()