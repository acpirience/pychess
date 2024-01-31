"""

Tests for board.py - get_FEN_from_board

"""

import pytest

from board import Board


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

    fen_string = test_board.get_FEN_from_board()

    assert fen_string == "8/8/8/8/8/8/8/8"


def test_start_board(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

    fen_string = test_board.get_FEN_from_board()

    assert fen_string == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


def test_four_rooks(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("r6r/8/8/8/8/8/8/R6R")

    fen_string = test_board.get_FEN_from_board()

    assert fen_string == "r6r/8/8/8/8/8/8/R6R"
