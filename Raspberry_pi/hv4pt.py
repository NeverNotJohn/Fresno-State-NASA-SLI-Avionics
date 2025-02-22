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
        
def data_to_audio(data, audio_array):
    """
    Loops through FLOATING NUM and adds chars to audio array
    """
    
    data = str(data)
    
    char_hash = {
        '0': 'audio/0.wav',
        '1': 'audio/1.wav',
        '2': 'audio/2.wav',
        '3': 'audio/3.wav',
        '4': 'audio/4.wav',
        '5': 'audio/5.wav',
        '6': 'audio/6.wav',
        '7': 'audio/7.wav',
        '8': 'audio/8.wav',
        '9': 'audio/9.wav',
        '.': 'audio/point.wav',        
    }
    
    for i in data:
        audio_array.append(char_hash[i])
        
        
def transmit_data(apogee, temp_of_site, time_of_landing, max_velocity):
    """
    Final Transmission of NASA Hit point
    
    THE REAL DEAL
    """
    
    print('Transmitting Data Points...')
    time.sleep(1)
    send_serial_data(COMMAND_TUNE_TO, PORT, BAUD_RATE)
    print("Tuning to 146.5200")
    time.sleep(1)
    send_serial_data(COMMAND_PTT_DOWN, PORT, BAUD_RATE)
    time.sleep(1)
    print("PTT Down")
    
    """ Make audio Array """
    audio_array = ["audio/call_sign.wav"]
    
    # Apogee
    audio_array.append("audio/apogee.wav")
    data_to_audio(apogee, audio_array)
    # FIXME: record feet
    audio_array.append("audio/meters.wav")
    
    # Temperature
    audio_array.append("audio/temperature.wav")
    data_to_audio(temp_of_site, audio_array)
    audio_array.append("audio/celcius.wav")
    
    # Time of Landing
    audio_array.append("audio/time_of_landing.wav")
    # FIXME
    hours = 1
    minutes = 2
    seconds = 3
    data_to_audio(hours, audio_array)
    audio_array.append("audio/hours.wav")
    data_to_audio(minutes, audio_array)
    audio_array.append("audio/minutes.wav")
    data_to_audio(seconds, audio_array)
    audio_array.append("audio/seconds.wav")
    
    # Max Velocity
    audio_array.append("audio/max_velocity.wav")
    data_to_audio(max_velocity, audio_array)
    # FIXME: record feet per second
    audio_array.append("audio/meters_per_second.wav")
    
    # Add Final Call Sign
    audio_array.append("audio/call_sign.wav")
    
    """ Combine Wave Files """
    combine_wav_files(audio_array, "audio/combined.wav")
    
    """ Send Audio!!! """
    send_wav_over_serial("audio/combined.wav", PORT, BAUD_RATE)
    
    # Let things Cook
    time.sleep(1)
    send_serial_data(COMMAND_PTT_UP, PORT, BAUD_RATE)
    print("PTT Up")
    
    
    
    
"""-------------------------MAIN-------------------------"""

def main():
    
    
    transmit_data(apogee=4010.12, temp_of_site=1241.21, time_of_landing=1, max_velocity=618.12)
    

if __name__ == "__main__":
    main()