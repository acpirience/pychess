"""

Tests for board.py - load_board_from_FEN

"""

import pytest

from board import Board
from piece import Piece


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

    for line in range(8):
        for col in range(8):
            assert not test_board.board_content[line][col], f"({line}, {col}) not empty"


def test_start_board(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

    # Rooks
    assert test_board.board_content[7][0] == Piece("R", "w"), "White Rook Expected"
    assert test_board.board_content[7][7] == Piece("R", "w"), "White Rook Expected"
    assert test_board.board_content[0][0] == Piece("R", "b"), "Black Rook Expected"
    assert test_board.board_content[0][7] == Piece("R", "b"), "Black Rook Expected"

    # Knights
    assert test_board.board_content[7][1] == Piece("N", "w"), "White Knight Expected"
    assert test_board.board_content[7][6] == Piece("N", "w"), "White Knight Expected"
    assert test_board.board_content[0][1] == Piece("N", "b"), "Black Knight Expected"
    assert test_board.board_content[0][6] == Piece("N", "b"), "Black Knight Expected"

    # Bishops
    assert test_board.board_content[7][2] == Piece("B", "w"), "White Bishop Expected"
    assert test_board.board_content[7][5] == Piece("B", "w"), "White Bishop Expected"
    assert test_board.board_content[0][2] == Piece("B", "b"), "Black Bishop Expected"
    assert test_board.board_content[0][5] == Piece("B", "b"), "Black Bishop Expected"

    # Queens
    assert test_board.board_content[7][3] == Piece("Q", "w"), "White Queen Expected"
    assert test_board.board_content[0][3] == Piece("Q", "b"), "Black Queen Expected"

    # Kings
    assert test_board.board_content[7][4] == Piece("K", "w"), "White King Expected"
    assert test_board.board_content[0][4] == Piece("K", "b"), "Black King Expected"

    for col in range(8):
        assert test_board.board_content[6][col] == Piece("P", "w"), "White Pawn Expected"
        assert test_board.board_content[1][col] == Piece("P", "b"), "Black Pawn Expected"

    for line in range(2, 6):
        for col in range(8):
            assert not test_board.board_content[line][col], f"({line}, {col}) not empty"
