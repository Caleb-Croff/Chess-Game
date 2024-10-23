from chess_piece import ChessPiece
from move import Move


class Bishop(ChessPiece):
    def __str__(self) -> str:
        return 'Bishop'

    def type(self) -> str:
        return 'Bishop'

    def is_valid_move(self, move: Move, board) -> bool:
        # inherits from parent function where if those occurences dont pass then they wont pass here
        if not super().is_valid_move(move, board):
            return False

        # Check if the move is a diagonal move (both row and column distances are equal)
        if abs(move.from_col - move.to_col) != abs(move.from_row - move.to_row):
            return False

        # Loop to check positions between move.from_row and move.to_row, move.from_col and move.to_col
        if move.to_row > move.from_row:
            step_row = 1
        else:
            step_row = -1

        if move.to_col > move.from_col:
            step_col = 1
        else:
            step_col = -1

        x = move.from_row + step_row
        y = move.from_col + step_col
        while (x, y) != (move.to_row, move.to_col):
            if board[x][y] is not None:
                return False
            x += step_row
            y += step_col

        return True
