"""

Tests for position.py - square_is_in_check

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
        "wKing can castle": False,
        "bKing can castle": False,
        "previous move": "",
    }


def test_square_is_attacked(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/1p4k1/8/8/8/8/8/r7")

    test_position = Position(test_board.board_content, test_flags)
    # rook
    assert test_position.square_is_attacked(
        test_board.board_content, "a8", str(test_flags["color"])
    )
    assert test_position.square_is_attacked(
        test_board.board_content, "a6", str(test_flags["color"])
    )
    assert test_position.square_is_attacked(
        test_board.board_content, "e1", str(test_flags["color"])
    )
    assert test_position.square_is_attacked(
        test_board.board_content, "h1", str(test_flags["color"])
    )
    # pawn
    assert test_position.square_is_attacked(
        test_board.board_content, "a6", str(test_flags["color"])
    )
    assert test_position.square_is_attacked(
        test_board.board_content, "c6", str(test_flags["color"])
    )
    # king
    assert test_position.square_is_attacked(
        test_board.board_content, "h8", str(test_flags["color"])
    )
    assert test_position.square_is_attacked(
        test_board.board_content, "h7", str(test_flags["color"])
    )
    assert test_position.square_is_attacked(
        test_board.board_content, "h6", str(test_flags["color"])
    )
