import streamlit as st
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import tempfile
import os
import threading

# Configuration
SAMPLE_RATE = 16000  # 16kHz is standard for speech recognition
CHANNELS = 1
FILENAME_PREFIX = "user_audio_"

def record_audio_non_blocking(max_duration=15, sample_rate=SAMPLE_RATE):
    """
    Records audio from the microphone with support for early stopping via a flag.
    Uses InputStream callback to continuously capture audio while checking st.session_state.stop_recording.
    Automatically stops after max_duration seconds.
    
    Args:
        max_duration (int): The maximum recording duration in seconds.
        sample_rate (int): The sample rate.
        
    Returns:
        str: The path to the saved WAV file, or None if recording failed.
    """
    try:
        # Initialize stop flag
        if 'stop_recording' not in st.session_state:
            st.session_state.stop_recording = False
        
        # Prepare audio buffer
        max_samples = int(max_duration * sample_rate)
        audio_buffer = np.zeros((max_samples, CHANNELS), dtype='int16')
        recorded_samples = [0]  # Use list to allow modification in nested function
        
        def audio_callback(indata, frames, time_info, status):
            """Callback for InputStream - copies audio to buffer."""
            if status:
                print(f"Audio callback status: {status}")
            
            # Stop if buffer is full or stop flag is set
            if recorded_samples[0] >= max_samples or st.session_state.stop_recording:
                raise sd.CallbackStop()
            
            # Copy audio data to buffer
            chunk_size = min(frames, max_samples - recorded_samples[0])
            audio_buffer[recorded_samples[0]:recorded_samples[0] + chunk_size] = indata[:chunk_size]
            recorded_samples[0] += chunk_size
        
        # Record using InputStream with callback - it will stop when buffer is full or callback raises CallbackStop
        try:
            with sd.InputStream(channels=CHANNELS, samplerate=sample_rate, callback=audio_callback, blocksize=2048):
                # Wait for recording to complete (callback will raise CallbackStop when done)
                # This loop is just a safety net; the callback controls the stop
                sd.sleep(max_duration * 1000)  # Sleep for max_duration milliseconds
        except Exception as stream_error:
            print(f"InputStream error: {stream_error}")
        
        # Extract only the recorded portion
        actual_recording = audio_buffer[:recorded_samples[0]]
        
        # Save the recording to a temporary WAV file
        if recorded_samples[0] > 0:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav", prefix=FILENAME_PREFIX)
            write(temp_file.name, sample_rate, actual_recording)
            return temp_file.name
        else:
            st.error("No audio was recorded.")
            return None
        
    except Exception as e:
        st.error(f"Could not record audio. Please ensure your microphone is connected and permissions are granted. Error: {e}")
        return None
    finally:
        # Reset the stop flag
        st.session_state.stop_recording = False


def record_audio(duration=15, sample_rate=SAMPLE_RATE):
    """
    Records audio from the microphone for a given duration (blocking version).
    
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
