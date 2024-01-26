"""

Tests for position.py - get_moves_for_piece => for the QUEEN

"""

import pytest

from board import Board
from position import Position


@pytest.fixture
def test_board() -> Board:
    # empty board used by tests
    return Board(True, "WOOD")


@pytest.fixture
def test_flags() -> dict[str, str | bool]:
    return {
        "color": "w",
        "in_check": "",
        "wKing can castle": True,
        "bKing can castle": True,
        "previous_move": "",
    }


def test_queen_move(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/4Q3/8/8/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == [
        "Qe4a4",
        "Qe4a8",
        "Qe4b1",
        "Qe4b4",
        "Qe4b7",
        "Qe4c2",
        "Qe4c4",
        "Qe4c6",
        "Qe4d3",
        "Qe4d4",
        "Qe4d5",
        "Qe4e1",
        "Qe4e2",
        "Qe4e3",
        "Qe4e5",
        "Qe4e6",
        "Qe4e7",
        "Qe4e8",
        "Qe4f3",
        "Qe4f4",
        "Qe4f5",
        "Qe4g2",
        "Qe4g4",
        "Qe4g6",
        "Qe4h1",
        "Qe4h4",
        "Qe4h7",
    ]


def test_black_queen_move(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/4q3/8/8/8")
    test_flags["color"] = "b"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == [
        "Qe4a4",
        "Qe4a8",
        "Qe4b1",
        "Qe4b4",
        "Qe4b7",
        "Qe4c2",
        "Qe4c4",
        "Qe4c6",
        "Qe4d3",
        "Qe4d4",
        "Qe4d5",
        "Qe4e1",
        "Qe4e2",
        "Qe4e3",
        "Qe4e5",
        "Qe4e6",
        "Qe4e7",
        "Qe4e8",
        "Qe4f3",
        "Qe4f4",
        "Qe4f5",
        "Qe4g2",
        "Qe4g4",
        "Qe4g6",
        "Qe4h1",
        "Qe4h4",
        "Qe4h7",
    ]


def test_queen_capture(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("r7/4p2p/8/8/r3Q2p/8/8/1b2n2b")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == [
        "Qe4b4",
        "Qe4b7",
        "Qe4c2",
        "Qe4c4",
        "Qe4c6",
        "Qe4d3",
        "Qe4d4",
        "Qe4d5",
        "Qe4e2",
        "Qe4e3",
        "Qe4e5",
        "Qe4e6",
        "Qe4f3",
        "Qe4f4",
        "Qe4f5",
        "Qe4g2",
        "Qe4g4",
        "Qe4g6",
        "Qe4xa4",
        "Qe4xa8",
        "Qe4xb1",
        "Qe4xe1",
        "Qe4xe7",
        "Qe4xh1",
        "Qe4xh4",
        "Qe4xh7",
    ]
