import speech_recognition as sr
import time
from typing import Callable, Optional
from faster_whisper import WhisperModel
import numpy as np
import threading


class SpeechToText:
    def __init__(self, handle_text_event: Callable[[str], None]) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=self.get_snowball_microphone_index(),
                                        sample_rate=16000,
                                        chunk_size=1024)
        self.fallback_model = WhisperModel("tiny", device="cpu")

        # output event logic
        self.handle_text_event = handle_text_event
        self.ready_to_handle_new_audio = threading.Event()
        self.ready_to_handle_new_audio.set()

    def get_snowball_microphone_index(self) -> Optional[int]:
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            if "Snowball" in name:
                return index
        return None

    def start_background_listening(self) -> Callable[[bool], None]:
        """Configure listening and start background tread.
        Returns a callable which can terminate the background thread."""
        with self.microphone as source:
            print("Calibrating to background noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        self.recognizer.pause_threshold = 1.0
        self.recognizer.dynamic_energy_threshold = True

        print("Start listening")
        return self.recognizer.listen_in_background(self.microphone, self.background_thread_speech_to_text)

    def background_thread_speech_to_text(self, recognizer: sr.Recognizer, audio: sr.AudioData) -> None:
        # blocks if not set
        self.ready_to_handle_new_audio.wait()

        try:
            text: str = self.recognizer.recognize_google(audio)
            self.send_text_to_main_thread(text)
        except sr.UnknownValueError:
            print("Could not parse")
        except sr.RequestError as e:
            print(f"Google Speech to Text failed: {e}, fall back to local Whisper")
            self.whisper_speech_to_text(audio)

    def whisper_speech_to_text(self, audio: sr.AudioData) -> None:
        try:
            audio_data = audio.get_raw_data(convert_rate=16000)
            audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            transcribed_audio_data, _ = self.fallback_model.transcribe(audio_array, language="en")
            text = " ".join(part.text for part in transcribed_audio_data).strip()
            self.send_text_to_main_thread(text)
        except sr.UnknownValueError:
            print("Could not parse")
        except sr.RequestError as e:
            print(f"Speech to Text Service error: {e}")

    def send_text_to_main_thread(self, text: str) -> None:
        # block incoming audio
        self.ready_to_handle_new_audio.clear()

        # process text in main thread
        print(f"\n[Voice Command]: {text}")
        self.handle_text_event(text)

        # stop blocking
        self.ready_to_handle_new_audio.set()


if __name__ == "__main__":
    stt = SpeechToText()
    stop_listening = stt.start_background_listening()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Terminate background thread
        stop_listening(wait_for_stop=False)