# 
# TTS Program - Generates a speech output (WAV file) of a given string
# 
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import os
import sys

INPUT_TEXT = "Hello World."
VOICE_ID = "Ak8Eltxy6be7fnMwVCCe"
OUTPUT_FILE = "speech_output.wav"

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def speak_text(text, output_file="speech_output.mp3", emotion_level=0.4):
    audio = client.text_to_speech.convert(
        VOICE_ID, 
        text=text,
        voice_settings=VoiceSettings(
            stability=emotion_level,  
            similarity_boost=0.75,
            style=0.3,
            use_speaker_boost=True
        )
    )
    
    with open(output_file, "wb") as f:
        for chunk in audio:
            f.write(chunk)

speak_text(INPUT_TEXT, OUTPUT_FILE, emotion_level=0.4)