from faster_whisper import WhisperModel
import os
import torch

# --- Configuration ---
# Model size: "tiny", "base", "small", "medium", "large-v2", "large-v3"
# "base" is a good balance of speed and accuracy for this use case.
MODEL_SIZE = "base"
COMPUTE_TYPE = "int8" # "float16" for GPU, "int8" for CPU
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize the model once
try:
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
except Exception as e:
    print(f"Error initializing Whisper model: {e}")
    model = None

def transcribe_audio(audio_path):
    """
    Transcribes an audio file using the faster-whisper model.
    
    Args:
        audio_path (str): The path to the audio file.
        
    Returns:
        str: The transcribed text, or an error message.
    """
    if not model:
        return "Speech transcription service is currently unavailable."
        
    if not os.path.exists(audio_path):
        return "Error: Audio file not found."

    try:
        segments, info = model.transcribe(audio_path, beam_size=5)
        
        print(f"Detected language '{info.language}' with probability {info.language_probability}")
        
        transcription = "".join(segment.text for segment in segments)
        
        return transcription.strip()
        
    except Exception as e:
        print(f"Error during transcription: {e}")
        return "Could not understand the audio. Please try speaking again."
    finally:
        # Clean up the temporary audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)
