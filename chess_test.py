import unittest
import pawn
from pawn import Pawn
from chess_model import ChessModel
from rook import Rook
from king import King
from bishop import Bishop
from knight import Knight
from queen import Queen
from chess_piece import ChessPiece
from player import Player
from move import Move
from chess_model import UndoException


class PawnTest(unittest.TestCase):
    def test_valid_move_same_col_single(self):
        chess_model = ChessModel()
        pawn = Pawn(Player.WHITE)
        chess_model.set_piece(6, 0, pawn)
        move = Move(6, 0, 5, 0)
        self.assertTrue(pawn.is_valid_move(move, chess_model.board))

    def test_valid_move_same_col_mult(self):
        chess_model = ChessModel()
        pawn = Pawn(Player.WHITE)
        chess_model.set_piece(6, 0, pawn)
        move = Move(6, 0, 4, 0)
        self.assertTrue(pawn.is_valid_move(move, chess_model.board))

    def test_invalid_move_single_diag(self):
        chess_model = ChessModel()
        pawn = Pawn(Player.WHITE)
        chess_model.set_piece(6, 0, pawn)
        move = Move(6, 0, 5, 1)
        self.assertFalse(pawn.is_valid_move(move, chess_model.board))

    def test_invalid_move_multi_diag(self):
        chess_model = ChessModel()
        pawn = Pawn(Player.WHITE)
        chess_model.set_piece(6, 0, pawn)
        move = Move(6, 0, 4, 2)
        self.assertFalse(pawn.is_valid_move(move, chess_model.board))

    def test_invalid_move_oob(self):
        chess_model = ChessModel()
        pawn = Pawn(Player.WHITE)
        chess_model.set_piece(0, 0, pawn)
        move = Move(0, 0, -1, 0)
        self.assertFalse(pawn.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_col_multi_forward(self):
        chess_model = ChessModel()
        pawn = Pawn(Player.WHITE)
        chess_model.set_piece(5, 0, pawn)
        move = Move(5, 0, 3, 0)
        self.assertFalse(pawn.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_loc(self):
        chess_model = ChessModel()
        pawn = Pawn(Player.WHITE)
        chess_model.set_piece(6, 0, pawn)
        move = Move(6, 0, 6, 0)
        self.assertFalse(pawn.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_player(self):
        chess_model = ChessModel()
        pawn = Pawn(Player.BLACK)
        chess_model.set_piece(2, 0, pawn)
        move = Move(1, 0, 2, 0)
        self.assertFalse(pawn.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_row_oob(self):
        chess_model = ChessModel()
        pawn = Pawn(Player.WHITE)
        chess_model.set_piece(6, 0, pawn)
        move = Move(6, 0, 6, -1)
        self.assertFalse(pawn.is_valid_move(move, chess_model.board))

    def test_invalid_move_side_to_side(self):
        chess_model = ChessModel()
        pawn = Pawn(Player.WHITE)
        chess_model.set_piece(6, 0, pawn)
        move = Move(6, 0, 6, 1)
        self.assertFalse(pawn.is_valid_move(move, chess_model.board))

    def test_invalid_move_wrong_from_loc(self):
        chess_model = ChessModel()
        pawn = Pawn(Player.WHITE)
        chess_model.set_piece(6, 0, pawn)
        move = Move(7, 0, 5, 0)
        self.assertFalse(pawn.is_valid_move(move, chess_model.board))

    def test_valid_invalid_move_same_col_single_backwards(self):
        chess_model = ChessModel()
        pawn = Pawn(Player.WHITE)
        chess_model.set_piece(6, 0, pawn)
        move = Move(6, 0, 7, 0)
        self.assertFalse(pawn.is_valid_move(move, chess_model.board))


class InCheckTest(unittest.TestCase):
    def test_check_simple_bishop(self):
        chess_model = ChessModel()
        chess_model.set_piece(1, 3, None)
        chess_model.set_piece(3, 1, Bishop(Player.WHITE))
        self.assertTrue(chess_model.in_check(Player.BLACK))

    def test_check_simple_bishop_blocked(self):
        chess_model = ChessModel()
        chess_model.set_piece(3, 1, Bishop(Player.WHITE))
        self.assertFalse(chess_model.in_check(Player.BLACK))

    def test_check_simple_knight(self):
        chess_model = ChessModel()
        chess_model.set_piece(2, 5, Knight(Player.WHITE))
        self.assertTrue(chess_model.in_check(Player.BLACK))

    def test_check_simple_pawn(self):
        chess_model = ChessModel()
        chess_model.set_piece(1, 5, Pawn(Player.WHITE))
        self.assertTrue(chess_model.in_check(Player.BLACK))

    def test_check_simple_queen(self):
        chess_model = ChessModel()
        chess_model.set_piece(1, 5, None)
        chess_model.set_piece(3, 7, Queen(Player.WHITE))
        self.assertTrue(chess_model.in_check(Player.BLACK))

    def test_check_simple_queen_blocked(self):
        chess_model = ChessModel()
        chess_model.set_piece(3, 7, Queen(Player.WHITE))
        self.assertFalse(chess_model.in_check(Player.BLACK))

    def test_check_simple_rook_col(self):
        chess_model = ChessModel()
        chess_model.set_piece(1, 4, None)
        chess_model.set_piece(5, 4, Rook(Player.WHITE))
        self.assertTrue(chess_model.in_check(Player.BLACK))

    def test_check_simple_rook_col_blocked(self):  # Pawn is blocking check
        chess_model = ChessModel()
        chess_model.set_piece(5, 4, Rook(Player.WHITE))
        self.assertFalse(chess_model.in_check(Player.BLACK))

    def test_check_simple_rook_row(self):
        chess_model = ChessModel()
        chess_model.set_piece(0, 0, Rook(Player.WHITE))
        chess_model.set_piece(0, 1, None)
        chess_model.set_piece(0, 2, None)
        chess_model.set_piece(0, 3, None)
        chess_model.set_piece(1, 0, None)
        self.assertTrue(chess_model.in_check(Player.BLACK))

    def test_check_simple_rook_row_blocked(self):  # Queen is blocking check
        chess_model = ChessModel()
        chess_model.set_piece(0, 0, Rook(Player.WHITE))
        chess_model.set_piece(0, 1, None)
        chess_model.set_piece(0, 2, None)
        chess_model.set_piece(1, 0, None)
        self.assertFalse(chess_model.in_check(Player.BLACK))


class IsCompleteTest(unittest.TestCase):
    def test_checkmate1(self):
        pass

    def test_checkmate2(self):
        pass

    def test_checkmate3(self):
        pass

    def test_checkmate4(self):
        pass

    def test_checkmate_simple(self):
        chess_model = ChessModel()
        chess_model.move(Move(6, 5, 5, 5))
        chess_model.move(Move(1, 4, 3, 4))
        chess_model.move(Move(6, 6, 4, 6))
        chess_model.move(Move(0, 3, 4, 7))
        self.assertTrue(chess_model.is_complete())

    def test_not_checkmate1v1(self):
        chess_model = ChessModel()
        chess_model.clear_board()
        chess_model.set_piece(0, 3, King(Player.BLACK))
        chess_model.set_piece(7, 3, King(Player.WHITE))
        self.assertTrue(chess_model.is_complete())


    def test_not_checkmate1v2(self):
        pass

    def test_not_checkmate2v1(self):
        pass

    def test_not_checkmate3v1(self):
        pass

    def test_not_checkmate3v2(self):
        pass

    def test_not_checkmate4v1(self):
        pass


class UndoTest(unittest.TestCase):
    def test_undo_pawn_promotion(self):
        chess_model = ChessModel()
        pawn = Pawn(Player.WHITE)
        chess_model.set_piece(1, 0, pawn)
        move = Move(1, 0, 0, 0)
        chess_model.move(move)  # Promote the pawn to a queen
        chess_model.undo()  # Undo the move
        self.assertIs(chess_model.piece_at(1, 0), pawn)

    def test_undo_too_many(self):
        chess_model = ChessModel()
        with self.assertRaises(UndoException):
            chess_model.undo()

    def test_undo_multiple_taken(self):
        chess_model = ChessModel()
        pawn = chess_model.piece_at(6, 4)
        pawn2 = chess_model.piece_at(1, 3)
        queen = chess_model.piece_at(0, 3)

        chess_model.move(Move(6, 4, 4, 4))
        chess_model.move(Move(1, 3, 3, 3))
        chess_model.move(Move(4, 3, 3, 3))
        chess_model.move(Move(0, 3, 3, 3))
        chess_model.undo()
        chess_model.undo()
        chess_model.undo()
        chess_model.undo()

        self.assertIs(chess_model.piece_at(6, 4), pawn)
        self.assertIs(chess_model.piece_at(1, 3), pawn2)
        self.assertIs(chess_model.piece_at(0, 3), queen)

    def test_undo_once(self):
        chess_model = ChessModel()
        piece = chess_model.piece_at(6, 4)
        chess_model.move(Move(6, 4, 4, 4))
        chess_model.undo()
        self.assertIs(chess_model.piece_at(6, 4), piece)

    def test_undo_once_take(self):
        chess_model = ChessModel()
        pawn = chess_model.piece_at(6, 4)
        pawn2 = chess_model.piece_at(1, 3)

        chess_model.move(Move(6, 4, 4, 4))
        chess_model.move(Move(1, 3, 3, 3))
        chess_model.move(Move(4, 3, 3, 3))
        chess_model.undo()
        chess_model.undo()
        chess_model.undo()

        self.assertIs(chess_model.piece_at(6, 4), pawn)
        self.assertIs(chess_model.piece_at(1, 3), pawn2)

    def test_undo_twice(self):
        chess_model = ChessModel()
        piece = chess_model.piece_at(6, 4)

        chess_model.move(Move(6, 4, 4, 4))
        chess_model.move(Move(6, 4, 3, 4))
        chess_model.undo()
        chess_model.undo()

        self.assertIs(chess_model.piece_at(6, 4), piece)


class RookTest(unittest.TestCase):
    def test_valid_move_same_col(self):
        chess_model = ChessModel()
        chess_model.set_piece(6, 0, None)
        chess_model.set_piece(1, 0, None)
        rook = chess_model.board[7][0]
        move = Move(7, 0, 0, 0)
        self.assertTrue(rook.is_valid_move(move, chess_model.board))

    def test_valid_move_same_row(self):
        chess_model = ChessModel()
        chess_model.set_piece(7, 1, None)
        chess_model.set_piece(7, 2, None)
        chess_model.set_piece(7, 3, None)
        chess_model.set_piece(7, 4, None)
        rook = chess_model.board[7][0]
        move = Move(7, 0, 7, 4)
        self.assertTrue(rook.is_valid_move(move, chess_model.board))

    def test_invalid_move_single_diagonal(self):
        chess_model = ChessModel()
        chess_model.set_piece(6, 1, None)
        rook = chess_model.board[7][0]
        move = Move(7, 0, 6, 1)
        self.assertFalse(rook.is_valid_move(move, chess_model.board))

    def test_invalid_move_mult_diagonal(self):
        chess_model = ChessModel()
        chess_model.set_piece(6, 1, None)
        rook = chess_model.board[7][0]
        move = Move(7, 0, 5, 2)
        self.assertFalse(rook.is_valid_move(move, chess_model.board))

    def test_invalid_move_diagonal_oob(self):
        chess_model = ChessModel()
        rook = chess_model.board[7][0]
        move = Move(7, 0, 8, -1)
        self.assertFalse(rook.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_column_oob(self):
        chess_model = ChessModel()
        rook = chess_model.board[7][0]
        move = Move(7, 0, 8, 0)
        self.assertFalse(rook.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_row_oob(self):
        chess_model = ChessModel()
        rook = chess_model.board[7][0]
        move = Move(7, 0, 7, -1)
        self.assertFalse(rook.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_col_blocked(self):  # Pawn is blocking the column
        chess_model = ChessModel()
        rook = chess_model.board[7][0]
        move = Move(7, 0, 5, 0)
        self.assertFalse(rook.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_loc(self):
        chess_model = ChessModel()
        rook = chess_model.board[7][0]
        move = Move(7, 0, 7, 0)
        self.assertFalse(rook.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_player(self):
        chess_model = ChessModel()
        rook = chess_model.board[7][0]
        move = Move(7, 0, 6, 0)
        self.assertFalse(rook.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_row_blocked(self):  # Knight and bishop are blocking the row
        chess_model = ChessModel()
        rook = chess_model.board[7][0]
        move = Move(7, 0, 7, 2)
        self.assertFalse(rook.is_valid_move(move, chess_model.board))

    def test_invalid_move_wrong_from_loc(self):
        chess_model = ChessModel()
        rook = chess_model.board[7][4]
        move = Move(4, 4, 7, 2)
        self.assertFalse(rook.is_valid_move(move, chess_model.board))


class KingTest(unittest.TestCase):
    def test_valid_move(self):
        chess_model = ChessModel()
        chess_model.set_piece(6, 4, None)
        king = chess_model.board[7][4]
        move = Move(7, 4, 6, 4)
        self.assertTrue(king.is_valid_move(move, chess_model.board))

    def test_invalid_move_multiple(self):
        chess_model = ChessModel()
        chess_model.set_piece(6, 4, None)
        king = chess_model.board[7][4]
        move = Move(7, 4, 5, 4)
        self.assertFalse(king.is_valid_move(move, chess_model.board))

    def test_invalid_move_oob(self):
        chess_model = ChessModel()
        king = chess_model.board[7][4]
        move = Move(7, 4, 8, 4)
        self.assertFalse(king.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_loc(self):
        chess_model = ChessModel()
        king = chess_model.board[7][4]
        move = Move(7, 4, 7, 4)
        self.assertFalse(king.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_player(self):
        chess_model = ChessModel()
        king = chess_model.board[7][4]
        move = Move(7, 4, 6, 4)
        self.assertFalse(king.is_valid_move(move, chess_model.board))

    def test_invalid_move_wrong_from_loc(self):
        chess_model = ChessModel()
        king = chess_model.board[7][4]
        move = Move(6, 4, 7, 4)
        self.assertFalse(king.is_valid_move(move, chess_model.board))


class BishopTest(unittest.TestCase):
    def valid_move_multiple(self):
        chess_model = ChessModel()
        chess_model.set_piece(6, 1, None)
        bishop = chess_model.board[7][2]
        move = Move(7, 2, 5, 0)
        self.assertTrue(bishop.is_valid_move(move, chess_model.board))

    def test_invalid_move_diag_blocked(self):
        chess_model = ChessModel()
        bishop = chess_model.board[7][2]
        move = Move(7, 2, 5, 0)
        self.assertFalse(bishop.is_valid_move(move, chess_model.board))

    def test_invalid_move_diagonal_oob(self):
        chess_model = ChessModel()
        chess_model.set_piece(6, 1, None)
        bishop = chess_model.board[7][2]
        move = Move(7, 2, 4, -1)
        self.assertFalse(bishop.is_valid_move(move, chess_model.board))

    def test_invalid_move_starting_oob(self):
        chess_model = ChessModel()
        bishop = chess_model.board[7][2]
        move = Move(8, 3, 5, 0)
        self.assertFalse(bishop.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_col(self):
        chess_model = ChessModel()
        bishop = chess_model.board[7][2]
        move = Move(6, 2, 7, 2)
        self.assertFalse(bishop.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_loc(self):
        chess_model = ChessModel()
        bishop = chess_model.board[7][2]
        move = Move(7, 2, 7, 2)
        self.assertFalse(bishop.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_player(self):
        chess_model = ChessModel()
        bishop = chess_model.board[7][2]
        move = Move(7, 2, 6, 3)
        self.assertFalse(bishop.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_row(self):
        chess_model = ChessModel()
        bishop = chess_model.board[7][2]
        move = Move(7, 2, 7, 3)
        self.assertFalse(bishop.is_valid_move(move, chess_model.board))

    def test_invalid_move_wrong_from_loc(self):
        chess_model = ChessModel()
        bishop = chess_model.board[7][2]
        move = Move(5, 2, 4, 3)
        self.assertFalse(bishop.is_valid_move(move, chess_model.board))


class KnightTest(unittest.TestCase):
    def test_knight_move_to_edge(self):
        chess_model = ChessModel()
        knight = chess_model.board[7][1]
        move = Move(7, 1, 5, 0)
        self.assertTrue(knight.is_valid_move(move, chess_model.board))

    def test_knight_move_from_edge(self):
        chess_model = ChessModel()
        knight = Knight(Player.WHITE)
        chess_model.set_piece(5, 0, knight)
        move = Move(5, 0, 3, 1)
        self.assertTrue(knight.is_valid_move(move, chess_model.board))

    def test_invalid_move_diagonal(self):
        chess_model = ChessModel()
        chess_model.set_piece(6, 0, None)
        knight = chess_model.board[7][1]
        move = Move(7, 1, 6, 0)
        self.assertFalse(knight.is_valid_move(move, chess_model.board))

    def test_invalid_move_oob(self):
        chess_model = ChessModel()
        knight = chess_model.board[7][1]
        move = Move(7, 1, 8, 3)
        self.assertFalse(knight.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_col(self):
        chess_model = ChessModel()
        knight = chess_model.board[7][1]
        move = Move(7, 1, 5, 1)
        self.assertFalse(knight.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_locs(self):
        chess_model = ChessModel()
        knight = chess_model.board[7][1]
        move = Move(7, 1, 7, 1)
        self.assertFalse(knight.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_player(self):
        chess_model = ChessModel()
        knight = chess_model.board[7][1]
        move = Move(7, 1, 6, 3)
        self.assertFalse(knight.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_row(self):
        chess_model = ChessModel()
        chess_model.set_piece(7, 3, None)
        knight = chess_model.board[7][1]
        move = Move(7, 1, 7, 3)
        self.assertFalse(knight.is_valid_move(move, chess_model.board))

    def test_invalid_move_wrong_from_loc(self):
        chess_model = ChessModel()
        knight = chess_model.board[7][1]
        move = Move(7, 0, 5, 2)
        self.assertFalse(knight.is_valid_move(move, chess_model.board))


class QueenTest(unittest.TestCase):
    def test_valid_move_same_row(self):
        chess_model = ChessModel()
        chess_model.set_piece(7, 0, None)
        chess_model.set_piece(7, 1, None)
        chess_model.set_piece(7, 2, None)
        queen = chess_model.board[7][3]
        move = Move(7, 3, 7, 0)
        self.assertTrue(queen.is_valid_move(move, chess_model.board))

    def test_valid_move_same_col(self):
        chess_model = ChessModel()
        chess_model.set_piece(6, 3, None)
        chess_model.set_piece(5, 3, None)
        queen = chess_model.board[7][3]
        move = Move(7, 3, 4, 3)
        self.assertTrue(queen.is_valid_move(move, chess_model.board))

    def test_invalid_move_diag_blocked(self):
        chess_model = ChessModel()
        chess_model.set_piece(6, 4, Pawn(Player.WHITE))
        queen = chess_model.board[7][3]
        move = Move(7, 3, 5, 5)
        self.assertFalse(queen.is_valid_move(move, chess_model.board))

    def test_invalid_move_diagonal_oob(self):
        chess_model = ChessModel()
        queen = chess_model.board[7][3]
        move = Move(7, 3, 8, 2)
        self.assertFalse(queen.is_valid_move(move, chess_model.board))

    def test_invalid_move_oob(self):
        chess_model = ChessModel()
        queen = chess_model.board[7][3]
        move = Move(7, 3, 7, 2)
        self.assertFalse(queen.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_col_blocked(self):
        chess_model = ChessModel()
        chess_model.set_piece(6, 3, Pawn(Player.WHITE))
        queen = chess_model.board[7][3]
        move = Move(7, 3, 5, 3)
        self.assertFalse(queen.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_locs(self):
        chess_model = ChessModel()
        queen = chess_model.board[7][3]
        move = Move(7, 3, 7, 3)
        self.assertFalse(queen.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_player(self):
        chess_model = ChessModel()
        chess_model.set_piece(6, 3, Pawn(Player.WHITE))
        chess_model.set_piece(7, 3, Queen(Player.WHITE))
        queen = chess_model.board[7][3]
        move = Move(7, 3, 6, 3)
        self.assertFalse(queen.is_valid_move(move, chess_model.board))

    def test_invalid_move_same_row_blocked(self):
        chess_model = ChessModel()
        chess_model.set_piece(7, 4, Pawn(Player.WHITE))
        chess_model.set_piece(7, 5, Pawn(Player.WHITE))
        queen = chess_model.board[7][3]
        move = Move(7, 3, 7, 6)
        self.assertFalse(queen.is_valid_move(move, chess_model.board))

    def test_invalid_move_wrong_from_loc(self):
        chess_model = ChessModel()
        queen = chess_model.board[7][3]
        move = Move(7, 3, 5, 4)
        self.assertFalse(queen.is_valid_move(move, chess_model.board))


class ChessModelInitTest(unittest.TestCase):
    def test_constructor_correct_layout(self):
        chess_model = ChessModel()

        expected_layout = [
            [Rook(Player.BLACK), Knight(Player.BLACK), Bishop(Player.BLACK), Queen(Player.BLACK),
             King(Player.BLACK), Bishop(Player.BLACK), Knight(Player.BLACK), Rook(Player.BLACK)],
            [Pawn(Player.BLACK)] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [Pawn(Player.WHITE)] * 8,
            [Rook(Player.WHITE), Knight(Player.WHITE), Bishop(Player.WHITE), Queen(Player.WHITE),
             King(Player.WHITE), Bishop(Player.WHITE), Knight(Player.WHITE), Rook(Player.WHITE)]]

        for row in range(8):
            for col in range(8):
                self.assertIsInstance(chess_model.board[row][col], type(expected_layout[row][col]))
                if chess_model.board[row][col] is not None:
                    self.assertEqual(chess_model.board[row][col].player, expected_layout[row][col].player)

    def test_constructor_correct_player(self):
        chess_model = ChessModel()
        self.assertEqual(chess_model.current_player, Player.WHITE)

    def test_nrows_val(self):
        chess_model = ChessModel()
        self.assertEqual(chess_model.nrows, 8)

    def test_ncols_val(self):
        chess_model = ChessModel()
        self.assertEqual(chess_model.ncols, 8)

    def test_nrows_int(self):
        chess_model = ChessModel()
        self.assertIsInstance(chess_model.nrows, int)

    def test_ncols_int(self):
        chess_model = ChessModel()
        self.assertIsInstance(chess_model.ncols, int)


class ChessModelValidMoveTest(unittest.TestCase):
    def test_invalid_move_into_check(self):
        chess_model = ChessModel()
        chess_model.clear_board()
        chess_model.set_piece(0, 0, King(Player.BLACK))
        chess_model.set_piece(7, 0, King(Player.WHITE))
        chess_model.set_piece(1, 1, Rook(Player.WHITE))
        king = chess_model.piece_at(0, 0)
        move = Move(0, 0, 1, 0)
        self.assertFalse(king.is_valid_move(move, chess_model.board))

    def test_invalid_move_none_loc(self):
        pass

    def test_invalid_move_stay_in_check(self):
        chess_model = ChessModel()
        chess_model.clear_board()
        chess_model.set_piece(2, 0, King(Player.BLACK))
        chess_model.set_piece(2, 1, Rook(Player.WHITE))
        chess_model.set_piece(3, 1, Rook(Player.WHITE))
        chess_model.set_piece(7, 0, King(Player.WHITE))
        king = chess_model.piece_at(0, 0)
        move = Move(2, 0, 3, 0)
        self.assertFalse(chess_model.is_valid_move(move))

    def test_valid_block_check(self):
        pass

    def testValidMove(self):
        pass


class MoveTest(unittest.TestCase):
    def test_move_pawn_promotion(self):
        chess_model = ChessModel()
        pawn = Pawn(Player.WHITE)
        chess_model.set_piece(1, 0, pawn)
        move = Move(1, 0, 0, 0)
        chess_model.move(move)

        queen = chess_model.piece_at(0, 0)
        self.assertIsInstance(queen, Queen)
        self.assertEqual(queen.player, Player.WHITE)

    def test_one_move(self):
        pass


if __name__ == '__main__':
    unittest.main()
