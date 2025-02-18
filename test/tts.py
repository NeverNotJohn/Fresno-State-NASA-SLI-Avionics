from gtts import gTTS
import numpy as np
import wave
import pydub

def text_to_speech(text, filename):
    # Generate speech using gTTS
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")

    # Convert mp3 to WAV
    sound = pydub.AudioSegment.from_mp3("temp.mp3")
    sound.export(filename, format="wav")

# Example usage
text_to_speech("Hello, this is a test.", "output.wav")
