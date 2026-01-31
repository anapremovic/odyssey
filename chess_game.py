import chess
from stockfish import Stockfish

TERMINATION_FLAG: str = "DONE"
STOCKFISH_EXE_PATH: str = "stockfish-windows-x86-64-avx2.exe"

class ChessGame:
    def __init__(self) -> None:
        self.board = chess.Board()
        self.stockfish = Stockfish(path=STOCKFISH_EXE_PATH)

    def play_chess(self) -> None:
        """Test function for running chess inside this module"""
        while True:
            print(self.board)
            user_move = input("Enter your move: ")

            stockfish_move = self.handle_user_move(user_move)
            if stockfish_move == TERMINATION_FLAG:
                break

    def handle_user_move(self, move: str) -> str:
        """Returns Stockfish move"""
        try:
            played_move = self.board.push_uci(move)
            print(f"You played {played_move}")
        except ValueError:
            print(f"{move} is invalid")
            return ""

        if self.board.is_game_over():
            self.game_over()
            return TERMINATION_FLAG

        stockfish_move = self.board.push_uci(self.get_stockfish_move())
        print(f"Stockfish played {stockfish_move}")

        if self.board.is_game_over():
            self.game_over()
            return TERMINATION_FLAG

        return str(stockfish_move)

    def get_stockfish_move(self) -> str:
        self.stockfish.set_fen_position(self.board.fen())
        return self.stockfish.get_best_move()

    def game_over(self) -> None:
        print("Thanks for playing\n")
        print(f"Result: {self.board.result()}")
        print(f"Outcome: {self.board.outcome().termination}")


if __name__ == "__main__":
    chess_game = ChessGame()
    chess_game.play_chess()