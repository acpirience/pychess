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
    return {"color": "w", "in_check": "", "previous_move": ""}


def test_full_board(test_board: Board, test_flags: dict[str, str]) -> None:
    # tbd when all pieces' moves are implemented
    test_board.load_board_from_FEN("rp4pr/pppppppp/8/8/8/8/PPPPPPPP/RP4PR")

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
