import chess
import random

termination_flag: str = "DONE"

class ChessGame:
    def __init__(self) -> None:
        self.board = chess.Board()

    def play_chess(self) -> None:
        """Test function for running chess inside this module"""
        while True:
            print(self.board)
            user_move = input("Enter your move: ")

            stockfish_move = self.handle_user_move(user_move)
            if stockfish_move == termination_flag:
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
            return termination_flag

        stockfish_move = self.get_stockfish_move()
        self.board.push(stockfish_move)
        print(f"Stockfish played {stockfish_move}")

        if self.board.is_game_over():
            self.game_over()
            return termination_flag

        return str(stockfish_move)

    def get_stockfish_move(self) -> chess.Move:
        # Temporarily return a random move
        legal_moves = list(self.board.legal_moves)
        return random.choice(legal_moves)

    def game_over(self) -> None:
        print("Thanks for playing\n")
        print(f"Result: {self.board.result()}")
        print(f"Outcome: {self.board.outcome().termination}")


if __name__ == "__main__":
    chess_game = ChessGame()
    chess_game.play_chess()