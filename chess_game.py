import chess
import chess.svg
from stockfish import Stockfish
import os
import threading
from flask import Flask
import logging
from time import sleep
import socket
import json 

TERMINATION_FLAG: str = "DONE"
STOCKFISH_EXE_PATH: str = "/usr/games/stockfish"
chess_web_app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
PORT = 5000

@chess_web_app.route('/')
def index():
    """Update UI every 500 milliseconds"""
    return """
    <html>
        <body style="background: #222; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
            <img id="board" src="/static/board.svg" style="height: 90vh;">
            <script>
                setInterval(() => {
                    const img = document.getElementById('board');
                    img.src = '/static/board.svg?v=' + new Date().getTime();
                }, 500);
            </script>
        </body>
    </html>
    """

def run_web_app():
    chess_web_app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except OSError:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class ChessGame:
    def __init__(self) -> None:
        ui_thread = threading.Thread(target=run_web_app, daemon=True)
        ui_thread.start()
        ip = get_ip()
        print(f"Starting server on {ip}:{PORT}")

        self.board = chess.Board()
        self.stockfish = Stockfish(path=STOCKFISH_EXE_PATH)
        if not os.path.exists('static'):
            os.makedirs('static')
        self.update_ui()
        self.last_move_san = None

    def play_chess(self) -> None:
        """Test function for running chess inside this module"""
        while True:
            print(self.board)
            user_move = input("Enter your move: ")

            stockfish_move = self.handle_user_move(user_move)
            if stockfish_move == TERMINATION_FLAG:
                break

    def handle_user_move(self, move: str) -> dict:
        try:
            # Support SAN
            move_obj = self.board.push_san(move)
        except (ValueError, chess.IllegalMoveError, chess.AmbiguousMoveError):
            try:
                # Support UCI
                uci_move = chess.Move.from_uci(move)
                if uci_move in self.board.legal_moves:
                    self.board.push(uci_move)
                    move_obj = uci_move
                else:
                    print(f"Move {move} is illegal.")
                    return TERMINATION_FLAG
            except (ValueError, TypeError):
                print(f"Move '{move}' is not valid SAN or UCI.")
                return ""

        user_san = self.board.san(move_obj)
        self.last_move_san = user_san
        print(f"You played {user_san}")

        self.update_ui()
        sleep(0.5)  # stall before Stockfish turn

        user_data = self.get_game_data()
        print("\n" + "="*60)
        print("="*60)
        print(json.dumps(user_data, indent=2))
        print("="*60 + "\n")

        if self.board.is_game_over():
            self.game_over()
            return TERMINATION_FLAG

        stockfish_uci = self.get_stockfish_move()
        stockfish_move_obj = chess.Move.from_uci(stockfish_uci)

        stockfish_san = self.board.san(stockfish_move_obj)
        self.last_move_san = stockfish_san

        self.board.push(stockfish_move_obj)
        print(f"Stockfish played {stockfish_san}")
        self.update_ui()

        if self.board.is_game_over():
            self.game_over()
            return TERMINATION_FLAG

        stockfish_data = self.get_game_data()
        print("\n" + "="*60)
        print("="*60)
        print(json.dumps(stockfish_data, indent=2))
        print("="*60 + "\n")

        return {
            'user': user_data,
            'stockfish': stockfish_data
            }

    def get_stockfish_move(self) -> str:
        self.stockfish.set_fen_position(self.board.fen())
        return self.stockfish.get_best_move()

    def game_over(self) -> None:
        print("Thanks for playing\n")
        print(f"Result: {self.board.result()}")
        print(f"Outcome: {self.board.outcome().termination}")

    def update_ui(self):
        last_move = self.board.peek() if self.board.move_stack else None
        board_svg = chess.svg.board(self.board, size=800, lastmove=last_move)
        with open("static/board.svg", "w") as f:
            f.write(board_svg)
    
    def get_game_data(self) -> dict:

        fen = self.board.fen()
        last_move_san = self.last_move_san

        self.stockfish.set_fen_position(fen)
        eval_data = self.stockfish.get_evaluation()

        return {
            "fen": fen,
            "last_move": last_move_san,
            "evaluation": eval_data
        }


if __name__ == "__main__":
    ui_thread_external = threading.Thread(target=run_web_app, daemon=True)
    ui_thread_external.start()

    ip_external = get_ip()
    print(f"Starting server on {ip_external}:{PORT}")

    chess_game = ChessGame()
    chess_game.play_chess()