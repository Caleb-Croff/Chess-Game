from chess_piece import ChessPiece
from player import Player
from move import Move


class Pawn(ChessPiece):
    def __init__(self, player):
        super().__init__(player)

    def __str__(self) -> str:
        return f"pawn"

    def type(self) -> str:
        return 'Pawn'

    # First move pawns can move forward two squares, then only one. They capture diagonally + en passant lol
    def is_valid_move(self, move: Move, board) -> bool:
        if not super().is_valid_move(move, board):
            return False
        if not isinstance(self, Pawn):
            return False

        # If the pawn is white, it moves up and starts on row 1, if it is black, it moves down and starts on row 6.
        if self.player == Player.BLACK:
            direction = 1
            starting_row = 1
        else:
            direction = -1
            starting_row = 6

        # Move forward one square
        # If the pawn stays on the same column, and the row it moves to minus its starting row equals the right direction(either 1 or -1).
        if move.to_col == move.from_col and (move.to_row - move.from_row) == direction:

            # If the square is empty.
            if board[move.to_row][move.to_col] is None:
                return True

        # If the pawn stays on the same column and is on the starting row(either 1 or 6).
        if move.to_col == move.from_col and move.from_row == starting_row:

            # If the pawn moves two squares, and the squares are not occupied.
            if abs(move.to_row - move.from_row) == 2 and board[move.from_row + direction][move.from_col] is None and board[move.to_row][move.to_col] is None:
                return True

        # Capture diagonally
        if abs(move.to_row - move.from_row) == 1 and abs(move.to_col - move.from_col) == 1:
            if move.to_row - move.from_row == direction and board[move.to_row][move.to_col] is not None and board[move.to_row][move.to_col].player != self.player:
                return True

        return False
