from chess_piece import ChessPiece
from move import Move


class King(ChessPiece):
    def __str__(self) -> str:
        return 'King'

    def type(self) -> str:
        return 'King'

    def is_valid_move(self, move: Move, board) -> bool:
        # Inherits from parent function to check basic move validity (like moving within board bounds)
        if not super().is_valid_move(move, board):
            return False

        # Checks if the King's move is exactly one square in any direction (including diagonally)
        if (abs(move.from_col - move.to_col) <= 1) and (abs(move.from_row - move.to_row) <= 1):
            return True
        else:
            return False
