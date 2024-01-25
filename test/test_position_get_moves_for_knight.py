"""

Tests for position.py - get_moves_for_piece => for the KNIGHT

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


def test_knight_move(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/3N4/8/8/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == ["Nb3", "Nb5", "Nc2", "Nc6", "Ne2", "Ne6", "Nf3", "Nf5"]


def test_black_knight_move(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/3n4/8/8/8")
    test_flags["color"] = "b"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == ["Nb3", "Nb5", "Nc2", "Nc6", "Ne2", "Ne6", "Nf3", "Nf5"]


def test_knight_capture(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/1n6/2n5/N7")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == ["Nxb3", "Nxc2"]


def test_knight_blocked(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("1n6/1Pp5/1pP5/1Pp5/1pP5/1Pp5/2P5/N7")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == []
