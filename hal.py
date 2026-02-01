from realtime_speech_to_text import SpeechToText
import time
from NLtoSANParser import parse
from chess_game import ChessGame


def run_hall():
    chess_engine = ChessGame()
    def process_one_turn(text: str) -> None:
        user_move_san = parse(text)
        print(f"Parsed {user_move_san}")

        if user_move_san is None:
            print("Could not parse")
            return
        
        dictionaries = chess_engine.handle_user_move(user_move_san)
        print(dictionaries)

    stt = SpeechToText(handle_text_event=process_one_turn)
    stop_listening = stt.start_background_listening()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Terminate background thread
        stop_listening(wait_for_stop=False)

if __name__ == "__main__":
    run_hall()