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
def test_flags() -> dict[str, str | bool]:
    return {"color": "w", "in_check": "", "previous_move": ""}


def test_full_board(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    # tbd when all pieces' moves are implemented
    test_board.load_board_from_FEN("rn4nr/pppppppp/8/8/8/8/PPPPPPPP/RN4NR")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == [
        "Nb1a3",
        "Nb1c3",
        "Ng1f3",
        "Ng1h3",
        "a2a3",
        "a2a4",
        "b2b3",
        "b2b4",
        "c2c3",
        "c2c4",
        "d2d3",
        "d2d4",
        "e2e3",
        "e2e4",
        "f2f3",
        "f2f4",
        "g2g3",
        "g2g4",
        "h2h3",
        "h2h4",
    ]
