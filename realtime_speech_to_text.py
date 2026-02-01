import speech_recognition as sr
import time
from typing import Callable, Optional
import os
import sys

class SpeechToText:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()

        # Suppress ALSA/JACK errors
        devnull = open(os.devnull, 'w')
        old_stderr = os.dup(2)
        os.dup2(devnull.fileno(), 2)

        self.microphone = sr.Microphone(device_index=self.get_snowball_microphone_index(),
                                        sample_rate=48000,
                                        chunk_size=1024)

        os.dup2(old_stderr, 2)
        os.close(old_stderr)
        devnull.close()

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
        try:
            text: str = self.recognizer.recognize_google(audio)
            print(f"\n[Voice Command]: {text}")
        except sr.UnknownValueError:
            print("No words parsed")
        except sr.RequestError as e:
            print(f"STT Service error: {e}")


if __name__ == "__main__":
    stt = SpeechToText()
    stop_listening = stt.start_background_listening()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Terminate background thread
        stop_listening(wait_for_stop=False)