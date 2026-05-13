import streamlit as st
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import tempfile
import os

# Configuration
SAMPLE_RATE = 16000  # 16kHz is standard for speech recognition
CHANNELS = 1
FILENAME_PREFIX = "user_audio_"

def record_audio(duration=15, sample_rate=SAMPLE_RATE):
    """
    Records audio from the microphone for a given duration.
    
    Args:
        duration (int): The recording duration in seconds.
        sample_rate (int): The sample rate.
        
    Returns:
        str: The path to the saved WAV file, or None if recording failed.
    """
    try:
        st.info(f"Recording for {duration} seconds... Please speak clearly.")
        
        # Record audio
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=CHANNELS, dtype='int16')
        sd.wait()  # Wait until recording is finished
        
        # Save the recording to a temporary WAV file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav", prefix=FILENAME_PREFIX)
        write(temp_file.name, sample_rate, recording)
        
        st.success("Recording complete.")
        return temp_file.name
        
    except Exception as e:
        st.error(f"Could not record audio. Please ensure your microphone is connected and permissions are granted. Error: {e}")
        return None
