import chess

class GameLogic:
    def __init__(self, fen=None):
        self.board = chess.Board(fen) if fen else chess.Board()

    def get_legal_moves(self):
        return list(self.board.legal_moves)

    def make_move(self, move):
        self.board.push(move)

    def undo_move(self):
        self.board.pop()

    def is_game_over(self):
        return self.board.is_game_over()

    def get_board(self):
        return self.board
