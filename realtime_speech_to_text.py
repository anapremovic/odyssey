import speech_recognition as sr
import time
from typing import Callable


class SpeechToText:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(sample_rate=48000)

    def start_background_listening(self) -> Callable[[bool], None]:
        """Configure listening and start background tread.
        Returns a callable which can terminate the background thread."""
        with self.microphone as source:
            print("Calibrating to background noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        self.recognizer.pause_threshold = 1.0
        self.recognizer.dynamic_energy_threshold = True

        return self.recognizer.listen_in_background(self.microphone, self.background_thread_speech_to_text)

    def background_thread_speech_to_text(self, audio: sr.AudioData) -> None:
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