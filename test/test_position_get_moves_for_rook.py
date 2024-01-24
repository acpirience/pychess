"""

Tests for position.py - get_moves_for_piece => for the ROOK

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


def test_rook_move(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/8/8/R7")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == [
        "Ra2",
        "Ra3",
        "Ra4",
        "Ra5",
        "Ra6",
        "Ra7",
        "Ra8",
        "Rb1",
        "Rc1",
        "Rd1",
        "Re1",
        "Rf1",
        "Rg1",
        "Rh1",
    ]


def test_black_rook_move(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/3r4/8/8/8/8")
    test_flags["color"] = "b"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == [
        "Ra5",
        "Rb5",
        "Rc5",
        "Rd1",
        "Rd2",
        "Rd3",
        "Rd4",
        "Rd6",
        "Rd7",
        "Rd8",
        "Re5",
        "Rf5",
        "Rg5",
        "Rh5",
    ]


def test_rook_capture(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("r7/8/8/8/8/8/8/R7")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()

    assert possible_moves == [
        "Ra2",
        "Ra3",
        "Ra4",
        "Ra5",
        "Ra6",
        "Ra7",
        "Rb1",
        "Rc1",
        "Rd1",
        "Re1",
        "Rf1",
        "Rg1",
        "Rh1",
        "Rxa8",
    ]


def test_black_rook_capture(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("r7/8/8/8/8/8/8/R7")
    test_flags["color"] = "b"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()

    assert possible_moves == [
        "Ra2",
        "Ra3",
        "Ra4",
        "Ra5",
        "Ra6",
        "Ra7",
        "Rb8",
        "Rc8",
        "Rd8",
        "Re8",
        "Rf8",
        "Rg8",
        "Rh8",
        "Rxa1",
    ]
