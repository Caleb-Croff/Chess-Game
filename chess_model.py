from enum import Enum
from player import Player
from move import Move
from chess_piece import ChessPiece
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King
import random


class MoveValidity(Enum):
    Valid = 1
    Invalid = 2
    MovingIntoCheck = 3
    StayingInCheck = 4
    Test = 5

    def __str__(self):
        if self.value == 2:
            return 'Invalid move.'

        if self.value == 3:
            return 'Invalid -- cannot move into check.'

        if self.value == 4:
            return 'Invalid -- must move out of check.'

        if self.value == 5:
            return 'Test'


class UndoException(Exception):
    pass


class ChessModel:
    def __init__(self):
        """
        Initialize the ChessModel class. This sets up the initial board with pieces in starting positions,
        sets the current player to white, defines board dimensions, initializes the message code to 'Valid',
        and prepares an empty move history.
        """
        self.board = [[], [], [], [], [], [], [], []]
        self.board[0] = [Rook(Player.BLACK), Knight(Player.BLACK), Bishop(Player.BLACK), Queen(Player.BLACK),
                         King(Player.BLACK), Bishop(Player.BLACK), Knight(Player.BLACK), Rook(Player.BLACK)]
        self.board[1] = [Pawn(Player.BLACK), Pawn(Player.BLACK), Pawn(Player.BLACK), Pawn(Player.BLACK),
                         Pawn(Player.BLACK), Pawn(Player.BLACK), Pawn(Player.BLACK), Pawn(Player.BLACK)]
        self.board[2] = [None, None, None, None, None, None, None, None]
        self.board[3] = [None, None, None, None, None, None, None, None]
        self.board[4] = [None, None, None, None, None, None, None, None]
        self.board[5] = [None, None, None, None, None, None, None, None]
        self.board[6] = [Pawn(Player.WHITE), Pawn(Player.WHITE), Pawn(Player.WHITE), Pawn(Player.WHITE),
                         Pawn(Player.WHITE), Pawn(Player.WHITE), Pawn(Player.WHITE), Pawn(Player.WHITE)]
        self.board[7] = [Rook(Player.WHITE), Knight(Player.WHITE), Bishop(Player.WHITE), Queen(Player.WHITE),
                         King(Player.WHITE), Bishop(Player.WHITE), Knight(Player.WHITE), Rook(Player.WHITE)]
        self.__player = Player.WHITE
        self.__nrows = 8
        self.__ncols = 8
        self.__message_code = MoveValidity.Valid
        self.__moves_history = []

    @property
    def nrows(self):
        """
        Property to get the number of rows on the chess board.

        Returns:
            int: Number of rows on the chess board.
        """
        return self.__nrows

    @property
    def ncols(self):
        """
        Property to get the number of columns on the chess board.

        Returns:
            int: Number of columns on the chess board.
        """
        return self.__ncols

    @property
    def current_player(self):
        """
        Property to get the current player.

        Returns:
            Player: The current player.
        """
        return self.__player

    @current_player.setter
    def current_player(self, new):
        """
        Setter for the current player.

        Parameters:
            new (Player): The new current player.
        """
        self.__player = new

    @property
    def messageCode(self):
        """
        Property to get the current message code, indicating the status of the last move or check state.

        Returns:
            MoveValidity: The current message code.
        """
        return self.__message_code

    @messageCode.setter
    def messageCode(self, new):
        """
        Setter for the message code.

        Parameters:
            new (MoveValidity): The new message code.
        """
        self.__message_code = new

    def clear_board(self):
        """
        Sets every spot on the board to None to empty the board
        """
        for x in range(self.nrows):
            for y in range(self.ncols):
                self.board[x][y] = None


    def copy_board(self):
        """
        Creates a copy of the current board state.

        Returns:
            list: A copy of the current board as a list of lists.
        """
        new_board = []
        for row in self.board:
            new_row = []
            for col in row:
                new_row.append(col)
            new_board.append(new_row)
        return new_board

    def one_vs_one(self):
        # Check if only kings are left to end the game
        for row in range(self.nrows):
            for col in range(self.ncols):
                if self.piece_at(row, col) is not None:
                    if self.piece_at(row,col) and self.piece_at(row,col).type() != "King":
                        return False
        return True

    def is_complete(self) -> bool:
        """
        Check if the game is complete by checkmate.

        Returns:
            bool: True if the game is complete, False otherwise.
        """
        if self.one_vs_one():
            return True
        if self.in_check(self.current_player):

            # Check if any legal move can get the king out of check
            for row in range(self.nrows):
                for col in range(self.ncols):
                    piece = self.piece_at(row, col)
                    if piece and piece.player == self.current_player:
                        for dest_row in range(self.nrows):
                            for dest_col in range(self.ncols):
                                move = Move(row, col, dest_row, dest_col)
                                if piece.is_valid_move(move, self.board):
                                    temp_board = self.copy_board()
                                    temp_board[dest_row][dest_col] = temp_board[row][col]
                                    temp_board[row][col] = None
                                    if not self.in_check_simulation(self.current_player, temp_board):
                                        return False  # Found a legal move, not checkmate
            return True  # No legal moves, it's checkmate

        return False

    def is_valid_move(self, move: Move) -> bool:
        """
        Determines if a given move is valid at a whole game level according to chess rules and the current board state.

        Parameters:
            move (Move): The move to be validated.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        moving_piece = self.piece_at(move.from_row, move.from_col)

        # Check if there's a piece at the source location
        if moving_piece is None:
            self.__message_code = MoveValidity.Invalid
            return False

        # Check if the move is valid for the piece
        if not moving_piece.is_valid_move(move, self.board):
            self.__message_code = MoveValidity.Invalid
            return False

        # Simulate the move
        temp_board = self.copy_board()
        temp_board[move.to_row][move.to_col] = moving_piece
        temp_board[move.from_row][move.from_col] = None

        # Check if the move results in the player's own king being in check
        if self.in_check_simulation(moving_piece.player, temp_board):
            # Determine the correct message code based on whether the king is already in check
            if self.in_check(moving_piece.player):
                self.__message_code = MoveValidity.StayingInCheck
            else:
                self.__message_code = MoveValidity.MovingIntoCheck
            return False
        # Checks to see if only the 2 kings are on the board if so no valid moves and game is over
        if self.one_vs_one():
            return False
        self.__message_code = MoveValidity.Valid
        return True

    def in_check(self, p: Player) -> bool:
        """
        Checks if the given player is currently in check.

        Parameters:
            p (Player): The player to check.

        Returns:
            bool: True if the player is in check, False otherwise.
        """
        king_position = None

        # Find the king's position
        for row in range(self.nrows):
            for col in range(self.ncols):
                piece = self.piece_at(row, col)
                if piece and piece.type() == 'King' and piece.player == p:
                    king_position = (row, col)
                    break

        king_row, king_col = king_position

        # Check if any opposing piece can move to the king's position
        for row in range(self.nrows):
            for col in range(self.ncols):
                piece = self.piece_at(row, col)
                if piece and piece.player != p:
                    move = Move(row, col, king_row, king_col)
                    if piece.is_valid_move(move, self.board):
                        return True  # The king is in check

        return False  # The king is not in check

    def in_check_simulation(self, player, board):
        """
        Checks if a player is currently in check on a simulated board.

        Parameters:
            player (Player): The player to check.
            board (list): The simulated board.

        Returns:
            bool: True if the player is in check in the simulation, False otherwise.
        """
        for row in range(self.nrows):
            for col in range(self.ncols):
                piece = board[row][col]
                if piece and piece.player != player:
                    for king_row in range(self.nrows):
                        for king_col in range(self.ncols):
                            king = board[king_row][king_col]
                            if king and king.type() == 'King' and king.player == player:
                                if piece.is_valid_move(Move(row, col, king_row, king_col), board):
                                    return True
        return False

    def move(self, move: Move):
        """
        Executes a chess move on the board.

        Parameters:
            move (Move): The move to be executed.
        """
        # Store the current game state before making the move
        self.__moves_history.append((self.copy_board(), self.current_player))

        # Take the player from move.from and set it equal to move.to
        self.board[move.to_row][move.to_col] = self.board[move.from_row][move.from_col]

        # Take the player from move.from and set it to have no piece
        self.board[move.from_row][move.from_col] = None

        # Takes instance of pawn and checks if it is moving to the end of the board. If so then promote it to a queen.
        if isinstance(self.board[move.to_row][move.to_col], Pawn) and (move.to_row == 0 or move.to_row == 7):
            self.board[move.to_row][move.to_col] = Queen(self.__player)

        # Switch to the next player
        self.set_next_player()

    def piece_at(self, row: int, col: int):
        """
        Retrieves the chess piece at a specific location on the board.

        Parameters:
            row (int): The row of the piece.
            col (int): The column of the piece.

        Returns:
            ChessPiece: The chess piece at the specified location, or None if no piece is present.
        """
        if 0 <= row < self.nrows and 0 <= col < self.ncols:
            return self.board[row][col]
        else:
            return None

    def set_next_player(self):
        """
        Switches the current player to the next player.
        """
        self.current_player = self.current_player.next()

    def set_piece(self, row: int, col: int, piece):
        """
        Places a chess piece at a specified location on the board.

        Parameters:
            row (int): The row to place the piece.
            col (int): The column to place the piece.
            piece (ChessPiece): The chess piece to be placed.

        Raises:
            TypeError: If the piece is not of type ChessPiece.
            ValueError: If the row or column is outside the board's dimensions.
        """
        if not isinstance(piece, ChessPiece) and piece is not None:
            raise TypeError('Piece must be of type ChessPiece')
        if row > self.__nrows or col > self.__ncols:
            raise ValueError
        if row < 0 or col < 0:
            raise ValueError

        self.board[row][col] = piece

    def undo(self):
        """
        Undoes the last move made in the game.

        Raises:
            UndoException: If there are no moves left to undo.
        """
        if len(self.__moves_history) == 0:
            raise UndoException("No moves left to undo")

        # Restore the game state to the most recent item in the moves history
        self.board, self.current_player = self.__moves_history.pop()

    def generate_all_valid_moves(self):
        """
        This method iterates over the entire chess board, finding all
        possible moves for the pieces of the current player. It checks each
        potential move for validity based on the rules of chess and the current
        state of the board.

        Returns:
            list: A list of Move objects representing all valid moves for the current player.
                  If no valid moves are available, returns an empty list.
        """
        player = self.current_player
        valid_moves = []
        for row in range(self.nrows):
            for col in range(self.ncols):
                piece = self.piece_at(row, col)
                if piece and piece.player == player:
                    for dest_row in range(self.nrows):
                        for dest_col in range(self.ncols):
                            move = Move(row, col, dest_row, dest_col)
                            if piece.is_valid_move(move, self.board) and self.is_valid_move(move):
                                valid_moves.append(move)
        return valid_moves

    def ai_move(self):
        """
        This method calls generate_all_valid_moves to get a list of all
        valid moves available for the current player. It then selects one move
        at random. If there are no valid moves available, the method will not execute any move.
        """
        valid_moves = self.generate_all_valid_moves()
        if valid_moves:
            random_move = random.choice(valid_moves)
            self.move(random_move)

