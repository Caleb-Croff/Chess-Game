from chess_piece import ChessPiece
from move import Move


class Knight(ChessPiece):
    def __str__(self) -> str:
        return 'Knight'

    def type(self) -> str:
        return 'Knight'

    # FIX ME
    # Knight moves two squares vertically or horizontally, and then one more square the opposite axis.
    def is_valid_move(self, move: Move, board) -> bool:
        if not super().is_valid_move(move, board):
            return False
        if not isinstance(self, Knight):
            return False
        if (move.from_row == move.to_row - 2 or move.from_row == move.to_row + 2) and (move.from_col == move.to_col - 1 or move.from_col == move.to_col + 1):
            return True
        elif (move.from_row == move.to_row - 1 or move.from_row == move.to_row + 1) and (move.from_col == move.to_col - 2 or (move.from_col == move.to_col + 2)):
            return True
        else:
            return False

