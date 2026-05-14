import streamlit as st
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import tempfile
import threading
import time

# --- Configuration ---
SAMPLE_RATE = 16000  # 16kHz, standard for speech recognition
CHANNELS = 1
FILENAME_PREFIX = "user_audio_"

# --- Thread-Safe State Management ---
# Using a class to hold state is cleaner than global variables and ensures
# that each recording session has its own state.
class RecorderState:
    def __init__(self):
        self.audio_buffer = []
        self.is_recording = False
        self.stop_requested = False
        self.lock = threading.Lock()

    def start(self):
        with self.lock:
            self.is_recording = True
            self.stop_requested = False
            self.audio_buffer = []

    def stop(self):
        with self.lock:
            self.is_recording = False
            self.stop_requested = True

    def add_data(self, data):
        if self.is_recording:
            self.audio_buffer.append(data)

    def get_data(self):
        with self.lock:
            return np.concatenate(self.audio_buffer, axis=0) if self.audio_buffer else np.array([])

# A single, shared state object for the recorder
recorder_state = RecorderState()

def set_stop_flag():
    """Public function to signal the recording thread to stop."""
    recorder_state.stop()
    print("Stop flag has been set.")

def is_recording():
    """Public function to check if recording is active."""
    return recorder_state.is_recording

def can_use_microphone():
    """Return True if a local audio input device is available."""
    try:
        devices = sd.query_devices()
        if not devices:
            return False
        for dev in devices:
            if isinstance(dev, dict):
                if dev.get("max_input_channels", 0) > 0:
                    return True
            elif len(dev) > 3 and dev[3] > 0:
                return True
        return False
    except Exception as e:
        print(f"Microphone detection error: {e}")
        return False


def record_audio_non_blocking(max_duration=15, sample_rate=SAMPLE_RATE):
    """
    Records audio in a non-blocking way using a dedicated thread.
    Communicates start/stop via a thread-safe state object.
    """
    if not can_use_microphone():
        print("No microphone input device is available.")
        return False
    
    def audio_callback(indata, frames, time_info, status):
        """This is called from the sounddevice thread for each audio chunk."""
        if status:
            print(f"Audio callback status: {status}")
        recorder_state.add_data(indata.copy())

    def recording_thread_main():
        """The main logic for the recording thread."""
        recorder_state.start()
        
        try:
            with sd.InputStream(samplerate=sample_rate, channels=CHANNELS, callback=audio_callback):
                start_time = time.time()
                while time.time() - start_time < max_duration:
                    if recorder_state.stop_requested:
                        print("Stop requested, breaking from recording loop.")
                        break
                    time.sleep(0.1) # Polling interval
        except Exception as e:
            st.error(f"An error occurred during recording: {e}")
            print(f"Error in recording thread: {e}")
        finally:
            # Always ensure the state is updated to 'not recording'
            print("Recording thread finished. Setting is_recording to False.")
            recorder_state.stop()

    # Start the recording in a background thread
    thread = threading.Thread(target=recording_thread_main, daemon=True)
    thread.start()
    
    # The main Streamlit thread does not wait/join. It just kicks off the recording.
    # The state is managed by the UI polling the `is_recording()` function.
    return True


def save_recording(sample_rate=SAMPLE_RATE):
    """
    Saves the content of the audio buffer to a temporary WAV file.
    This should be called after the recording has stopped.
    """
    audio_data = recorder_state.get_data()

    if audio_data.size == 0:
        st.warning("No audio was recorded. The microphone might not have captured any sound.")
        return None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", prefix=FILENAME_PREFIX) as temp_file:
            write(temp_file.name, sample_rate, audio_data)
            print(f"Audio successfully saved to {temp_file.name}")
            return temp_file.name
    except Exception as e:
        st.error(f"Failed to save the recorded audio. Error: {e}")
        print(f"Error saving WAV file: {e}")
        return None


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
