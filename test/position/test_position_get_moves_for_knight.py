"""

Tests for position.py - get_moves_for_piece => for the KNIGHT

"""

import pytest

from board import Board
from common import FlagsT
from position import Position


@pytest.fixture
def test_board() -> Board:
    # empty board used by tests
    return Board("WOOD")


@pytest.fixture
def test_flags() -> FlagsT:
    return {
        "color": "w",
        "wKing_can_castle": True,
        "bKing_can_castle": True,
        "previous_move": "",
        "game_type": "PVP",
        "player_color": "w",
    }


def test_knight_move(test_board: Board, test_flags: FlagsT) -> None:
    test_board.load_board_from_FEN("8/8/8/8/3N4/8/8/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()
    chess_moves = [x.chess_move for x in possible_moves]
    chess_moves.sort()

    assert chess_moves == [
        "Nd4b3",
        "Nd4b5",
        "Nd4c2",
        "Nd4c6",
        "Nd4e2",
        "Nd4e6",
        "Nd4f3",
        "Nd4f5",
    ]


def test_black_knight_move(test_board: Board, test_flags: FlagsT) -> None:
    test_board.load_board_from_FEN("8/8/8/8/3n4/8/8/8")
    test_flags["color"] = "b"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()
    chess_moves = [x.chess_move for x in possible_moves]
    chess_moves.sort()

    assert chess_moves == [
        "Nd4b3",
        "Nd4b5",
        "Nd4c2",
        "Nd4c6",
        "Nd4e2",
        "Nd4e6",
        "Nd4f3",
        "Nd4f5",
    ]


def test_knight_capture(test_board: Board, test_flags: FlagsT) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/1n6/2n5/N7")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()
    chess_moves = [x.chess_move for x in possible_moves]
    chess_moves.sort()

    assert chess_moves == ["Na1xb3", "Na1xc2"]


def test_knight_blocked(test_board: Board, test_flags: FlagsT) -> None:
    test_board.load_board_from_FEN("1n6/1Pp5/1pP5/1Pp5/1pP5/1Pp5/2P5/N7")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()
    chess_moves = [x.chess_move for x in possible_moves]
    chess_moves.sort()

    assert chess_moves == []
