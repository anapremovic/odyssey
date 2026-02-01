from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import os

INPUT_TEXT = "I'm afraid I can't do that, Dave."
VOICE_ID = "pNInz6obpgDQGcFmaJgB"
OUTPUT_FILE = "speech_output.wav"

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def speak(text, output_file, emotion_level=0.4):
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

speak(INPUT_TEXT, OUTPUT_FILE, emotion_level=0.4)