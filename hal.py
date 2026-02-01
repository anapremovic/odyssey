from realtime_speech_to_text import SpeechToText
import time
from NLtoSANParser import parse
from chess_game import ChessGame
from SANtoVoiceLine import DicttoVoiceLine
import text_to_speech
import subprocess
import threading

enum

def run_hall():
    chess_engine = ChessGame()
    exit_event = threading.Event()

    def process_one_turn(text: str) -> None:
        if not text:
            return

        # If user says quit or exit, stop the STT and signal main loop to exit
        lower_text = text.lower()
        if "quit" in lower_text or "exit" in lower_text or "close" in lower_text:
            hal_text = "Very well, game terminated."
            print("HAL says:\n" + hal_text)
            try:
                text_to_speech.speak_text(hal_text, "HAL_exit.mp3")
                subprocess.run(['mpg123', '-q', '-o', 'alsa', '-a', 'hw:0,0', 'HAL_exit.mp3'])
            except Exception:
                pass
            try:
                stop_listening(wait_for_stop=False)
            except Exception:
                pass
            exit_event.set()
            return

        user_move_san = parse(text)
        print(f"Parsed {user_move_san}")

        if user_move_san is None:
            print("Could not parse")
            return
        
        dictionaries = chess_engine.handle_user_move(user_move_san)

        if isinstance(dictionaries, dict):
            halLine = DicttoVoiceLine(dictionaries)
            print("HAL says:\n", halLine)
            text_to_speech.speak_text(halLine, "HAL_speech_output.mp3")
            subprocess.run(['mpg123', '-q', '-o', 'alsa', '-a', 'hw:0,0', 'HAL_speech_output.mp3'])

    stt = SpeechToText(handle_text_event=process_one_turn)
    stop_listening = stt.start_background_listening()

    try:
        while not exit_event.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Terminate background thread
        stop_listening(wait_for_stop=False)

if __name__ == "__main__":
    run_hall()