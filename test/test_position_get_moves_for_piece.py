"""

Tests for position.py - get_moves_for_piece

"""

import pytest

from board import Board
from position import Position


@pytest.fixture
def test_board() -> Board:
    # empty board used by tests
    return Board(True, "WOOD")


@pytest.fixture
def test_flags() -> dict[str, str]:
    return {"color": "w", "in_check": ""}


def test_move_pawns_alone(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/8/PPPPPPPP/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == [
        "a3",
        "a4",
        "b3",
        "b4",
        "c3",
        "c4",
        "d3",
        "d4",
        "e3",
        "e4",
        "f3",
        "f4",
        "g3",
        "g4",
        "h3",
        "h4",
    ]


def test_move_pawns_blocked(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/p1p1p1p1/P1P1P1P1/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == []


def test_move_pawns_mixed(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/6p1/4p3/2p5/p7/P1P1P1P1/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == ["c3", "e3", "e4", "g3", "g4"]
