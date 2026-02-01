from realtime_speech_to_text import SpeechToText
import time

def run_hall():
    stt = SpeechToText()
    stop_listening = stt.start_background_listening()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Terminate background thread
        stop_listening(wait_for_stop=False)

if __name__ == "__main__":
    run_hall()