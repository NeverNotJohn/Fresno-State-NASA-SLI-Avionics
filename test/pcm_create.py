import wave
import numpy as np
import simpleaudio as sa
import serial

def create_pcm_audio(filename, data, sample_rate=22050, sample_width=2, num_channels=1):
    """
    Creates a PCM audio file.

    Args:
        filename (str): The name of the file to create.
        data (np.array): The audio data as a NumPy array.
        sample_rate (int): The sample rate of the audio.
        sample_width (int): The sample width in bytes.
        num_channels (int): The number of channels.
    """
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(num_channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.setcomptype('NONE', 'Uncompressed')
        
        # Convert data to bytes
        if sample_width == 2:
            data = (data * 32767).astype(np.int16).tobytes() # 16-bit
        elif sample_width == 1:
             data = (data * 127).astype(np.int8).tobytes() # 8-bit
        else:
            raise ValueError("Unsupported sample width")
        
        wf.writeframes(data)

def send_wav_over_serial(wav_file_path, port='COM3', baud_rate=230400, chunk_size=1):
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
                #print(f"Sent {len(chunk)} bytes")

        print("File transmission complete.")

    except Exception as e:
        print(f"Error: {e}")

# Example usage:
# send_wav_over_serial("audio.wav", "/dev/ttyUSB0")  # Change port as needed


if __name__ == '__main__':

    # Generate a simple sine wave
    sample_rate = 22050
    duration = 1
    frequency = 432
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    # Create the PCM audio file
    create_pcm_audio('sine_wave.wav', audio_data, sample_rate)
 