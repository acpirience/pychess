"""

Tests for position.py - fill_move_map

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
        "in_check": "",
        "wKing can castle": True,
        "bKing can castle": True,
        "previous_move": "",
    }


def test_move_map_start(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

    test_position = Position(test_board.board_content, test_flags)
    move_map = test_position.move_map

    # pawns
    assert (6, 0) in move_map
    assert (6, 1) in move_map
    chess_moves = [x.chess_move for x in move_map[(6, 2)]]

    assert "c2c3" in chess_moves
    assert "c2c4" in chess_moves

    # Knights
    assert (7, 1) in move_map
    assert (7, 6) in move_map
    chess_moves = [x.chess_move for x in move_map[(7, 1)]]

    assert "Nb1c3" in chess_moves
    assert "Nb1a3" in chess_moves

    # king
    assert (7, 4) not in move_map


def test_move_map_castle(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R")

    test_position = Position(test_board.board_content, test_flags)
    move_map = test_position.move_map

    # king
    assert (7, 4) in move_map
    chess_moves = [x.chess_move for x in move_map[(7, 4)]]

    assert "Ke1f1" in chess_moves
    assert "0-0" in chess_moves
