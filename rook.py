from chess_piece import ChessPiece
from move import Move


class Rook(ChessPiece):
    def __str__(self) -> str:
        return 'Rook'

    def type(self) -> str:
        return 'Rook'

    def is_valid_move(self, move: Move, board) -> bool:
        # inherits from parent function where if those occurences dont pass then they wont pass here
        if not super().is_valid_move(move, board):
            return False

        if move.from_row != move.to_row and move.from_col != move.to_col:
            return False

        if move.from_row == move.to_row:
            row = 0
        elif move.from_row < move.to_row:
            row = 1
        else:
            row = -1

        if move.from_col == move.to_col:
            col = 0
        elif move.from_col < move.to_col:
            col = 1
        else:
            col = -1

        x = move.from_row + row
        y = move.from_col + col

        while (x, y) != (move.to_row, move.to_col):
            if board[x][y] is not None:
                return False
            x += row
            y += col

        return True