"""

Tests for position.py - get_moves_for_piece => for the BISHOP

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
    return {"color": "w", "in_check": "", "previous_move": ""}


def test_bishop_move(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/3B4/8/8/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == [
        "Bd4a1",
        "Bd4a7",
        "Bd4b2",
        "Bd4b6",
        "Bd4c3",
        "Bd4c5",
        "Bd4e3",
        "Bd4e5",
        "Bd4f2",
        "Bd4f6",
        "Bd4g1",
        "Bd4g7",
        "Bd4h8",
    ]


def test_black_bishop_move(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/3b4/8/8/8")
    test_flags["color"] = "b"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == [
        "Bd4a1",
        "Bd4a7",
        "Bd4b2",
        "Bd4b6",
        "Bd4c3",
        "Bd4c5",
        "Bd4e3",
        "Bd4e5",
        "Bd4f2",
        "Bd4f6",
        "Bd4g1",
        "Bd4g7",
        "Bd4h8",
    ]


def test_bishop_capture(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/2b6/8/B7")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == ["Ba1b2", "Ba1xc3"]


def test_blocked_blocked(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("1p6/1P6/1P6/1P6/1P6/1P6/1P6/B7")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == []
