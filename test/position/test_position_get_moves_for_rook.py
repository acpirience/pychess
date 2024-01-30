"""

Tests for position.py - get_moves_for_piece => for the ROOK

"""

import pytest

from board import Board
from position import Position


@pytest.fixture
def test_board() -> Board:
    # empty board used by tests
    return Board("WOOD")


@pytest.fixture
def test_flags() -> dict[str, str | bool]:
    return {
        "color": "w",
        "in_check": "",
        "wKing can castle": True,
        "bKing can castle": True,
        "previous_move": "",
    }


def test_rook_move(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/8/8/R7")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()
    chess_moves = [x.chess_move for x in possible_moves]
    chess_moves.sort()

    assert chess_moves == [
        "Ra1a2",
        "Ra1a3",
        "Ra1a4",
        "Ra1a5",
        "Ra1a6",
        "Ra1a7",
        "Ra1a8",
        "Ra1b1",
        "Ra1c1",
        "Ra1d1",
        "Ra1e1",
        "Ra1f1",
        "Ra1g1",
        "Ra1h1",
    ]


def test_black_rook_move(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/3r4/8/8/8/8")
    test_flags["color"] = "b"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()
    chess_moves = [x.chess_move for x in possible_moves]
    chess_moves.sort()

    assert chess_moves == [
        "Rd5a5",
        "Rd5b5",
        "Rd5c5",
        "Rd5d1",
        "Rd5d2",
        "Rd5d3",
        "Rd5d4",
        "Rd5d6",
        "Rd5d7",
        "Rd5d8",
        "Rd5e5",
        "Rd5f5",
        "Rd5g5",
        "Rd5h5",
    ]


def test_rook_capture(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("r7/8/8/8/8/8/8/R7")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()
    chess_moves = [x.chess_move for x in possible_moves]
    chess_moves.sort()

    assert chess_moves == [
        "Ra1a2",
        "Ra1a3",
        "Ra1a4",
        "Ra1a5",
        "Ra1a6",
        "Ra1a7",
        "Ra1b1",
        "Ra1c1",
        "Ra1d1",
        "Ra1e1",
        "Ra1f1",
        "Ra1g1",
        "Ra1h1",
        "Ra1xa8",
    ]


def test_black_rook_capture(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("r7/8/8/8/8/8/8/R7")
    test_flags["color"] = "b"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()
    chess_moves = [x.chess_move for x in possible_moves]
    chess_moves.sort()

    assert chess_moves == [
        "Ra8a2",
        "Ra8a3",
        "Ra8a4",
        "Ra8a5",
        "Ra8a6",
        "Ra8a7",
        "Ra8b8",
        "Ra8c8",
        "Ra8d8",
        "Ra8e8",
        "Ra8f8",
        "Ra8g8",
        "Ra8h8",
        "Ra8xa1",
    ]
