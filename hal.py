from realtime_speech_to_text import SpeechToText
import time

def parse_natural_language(text: str):
    print(f"Natural language: {text}")

def run_hall():
    stt = SpeechToText(handle_text_event=parse_natural_language)
    stop_listening = stt.start_background_listening()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Terminate background thread
        stop_listening(wait_for_stop=False)

if __name__ == "__main__":
    run_hall()