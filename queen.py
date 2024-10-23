from chess_piece import ChessPiece
from move import Move


class Queen(ChessPiece):
    def __str__(self) -> str:
        return 'Queen'

    def type(self) -> str:
        return 'Queen'

    # FIX ME
    def is_valid_move(self, move: Move, board) -> bool:
        if not super().is_valid_move(move, board):
            return False
        if not isinstance(self, Queen):
            return False
        # Checks for movements that resemble the bishops movement(Diagonals)
        if abs(move.from_col - move.to_col) == abs(move.from_row - move.to_row):
            # Determines if you need to add or subtract values when iterating to the destination piece
            if move.to_row > move.from_row:
                row = 1
            else:
                row = -1

            if move.to_col > move.from_col:
                col = 1
            else:
                col = -1
            # starts the positions we are iterating through one piece ahead so we dont check the initial from location
            x = move.from_row + row
            y = move.from_col + col
            #Iterate through the x and y values to check nothing is in the way of the destination
            while (x, y) != (move.to_row, move.to_col):
                if board[x][y] is not None:
                    return False
                x += row
                y += col

            return True
            #End of Bishop Movement
        #Start of Rook movement
        else:
            # sets x and y values to move.from values
            x = move.from_row
            y = move.from_col

            # Checks if you are moving columns or up and down
            if move.from_row == move.to_row:
                # While loop iterates over the y values till it reaches the destination
                while (x, y) != (move.to_row, move.to_col):
                    if move.to_col > move.from_col:
                        y += 1
                    else:
                        y -= 1
                    if board[x][y] is not None and (x, y) != (move.to_row, move.to_col):
                        return False
                # if nothing is in the way of moving to the piece returns True
                return True
            # Checks if you are moving rows or left and right
            if move.from_col == move.to_col:
                # While loop iterates over the x values till it reaches the destination
                while (x, y) != (move.to_row, move.to_col):
                    if move.to_row > move.from_row:
                        x += 1
                    else:
                        x -= 1
                    if board[x][y] is not None and (x, y) != (move.to_row, move.to_col):
                        return False
                # if nothing is in the way of moving to the piece returns True
                return True
            # End of Rook Movements
