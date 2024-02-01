"""

Tests for position.py - pretty_print_board

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
        "wKing can castle": True,
        "bKing can castle": True,
        "previous_move": "",
    }


def test_empty_board(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/8/8/8")

    assert (
        Position.pretty_print_board(test_board.board_content) == "\n"
        "                        \n"
        "                        \n"
        "                        \n"
        "                        \n"
        "                        \n"
        "                        \n"
        "                        \n"
        "                        \n"
    )


def test_start_board(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

    assert (
        Position.pretty_print_board(test_board.board_content)
        == "\n"
           "Rb Nb Bb Qb Kb Bb Nb Rb \n"
           "Pb Pb Pb Pb Pb Pb Pb Pb \n"
           "                        \n"
           "                        \n"
           "                        \n"
           "                        \n"
           "Pw Pw Pw Pw Pw Pw Pw Pw \n"
           "Rw Nw Bw Qw Kw Bw Nw Rw \n"
    )
