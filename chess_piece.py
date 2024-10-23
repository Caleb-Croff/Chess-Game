from abc import ABC, abstractmethod
from move import Move
from player import Player


class ChessPiece(ABC):
    def __init__(self, player: Player):
        self.__player = player

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, new):
        self.__player = new

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def type(self) -> str:
        pass

    def is_valid_move(self, move: Move, board: list) -> bool:
        """
        :param move:
        :param board:
        :return:
        """
        """board is a list with a nested list within representing the position of a piece
        row is a list in board and col is the element within row Ex. board[row0[col0],row1[col1]...]
        """
        # the if statement checks to see if you input a starting move is a viable spot on the board and if the destination spot is a viable place on the board. If not then it returns false
        if not (0 <= move.from_row < len(board) and 0 <= move.from_col < len(board[0]) and 0 <= move.to_row < len(board) and 0 <= move.to_col < len(board[0])):
            return False
        # if you try to move a piece to where is already sits it returns it as false
        if move.from_row == move.to_row and move.from_col == move.to_col:
            return False
        # verifies that self piece is located at starting location in move
        if board[move.from_row][move.from_col] != self:
            return False
        # checks if the position you are moving to has a piece in it. and if the position you are moving to is type of your own player. If these occur then it returns false
        if board[move.to_row][move.to_col] is not None and board[move.to_row][move.to_col].player == self.player:
            return False
        return True
