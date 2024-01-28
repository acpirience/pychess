"""

Tests for position.py - get_moves_for_piece => for the PAWN

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


def test_move_pawns_alone(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/8/PPPPPPPP/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    possible_moves.sort()
    assert possible_moves == [
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


def test_move_pawns_blocked(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/p1p1p1p1/P1P1P1P1/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    possible_moves.sort()
    assert possible_moves == []


def test_move_pawns_mixed(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/6p1/4p3/2p5/p5P1/P1P1P1P1/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    possible_moves.sort()
    assert possible_moves == ["c2c3", "e2e3", "e2e4", "g3g4"]


def test_move_pawns_take(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/pppppppp/4P3/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    possible_moves.sort()
    assert possible_moves == ["e2xd3", "e2xf3"]


def test_black_pawns_move_and_take(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/1p4p1/PPP4p/8/8/8/8/8")
    test_flags["color"] = "b"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    possible_moves.sort()
    assert possible_moves == ["b7xa6", "b7xc6", "g7g5", "g7g6", "h6h5"]


def test_pawns_capture_en_passant(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/pPp5/8/8/8/8")
    test_flags["previous_move"] = "a7a5"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    possible_moves.sort()
    assert possible_moves == ["b5b6", "b5xa6"]


def test_black_pawns_capture_en_passant(
    test_board: Board, test_flags: dict[str, str | bool]
) -> None:
    test_board.load_board_from_FEN("8/8/8/8/4PpP1/8/8/8")
    test_flags["color"] = "b"
    test_flags["previous_move"] = "e2e4"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    possible_moves.sort()
    assert possible_moves == ["f4f3", "f4xe3"]
