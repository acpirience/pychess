"""

Tests for position.py - get_moves_for_piece => for the PAWN

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


def test_move_pawns_alone(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/8/PPPPPPPP/8")

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


def test_move_pawns_blocked(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/p1p1p1p1/P1P1P1P1/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == []


def test_move_pawns_mixed(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/6p1/4p3/2p5/p5P1/P1P1P1P1/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == ["c3", "e3", "e4", "g4"]


def test_move_pawns_take(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/pppppppp/4P3/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == ["exd3", "exf3"]


def test_black_pawns_move_and_take(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/1p4p1/PPP4p/8/8/8/8/8")
    test_flags["color"] = "b"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == ["bxa6", "bxc6", "g5", "g6", "h5"]


def test_pawns_capture_en_passant(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/pPp5/8/8/8/8")
    test_flags["previous_move"] = "a5"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == ["b6", "bxa6"]


def test_black_pawns_capture_en_passant(test_board: Board, test_flags: dict[str, str]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/4PpP1/8/8/8")
    test_flags["color"] = "b"
    test_flags["previous_move"] = "e4"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_possible_moves()

    possible_moves.sort()
    assert possible_moves == ["f3", "fxe3"]
