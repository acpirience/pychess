"""

Tests for position.py - get_moves_for_piece => for the KING

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
    return {
        "color": "w",
        "in_check": "",
        "wKing can castle": True,
        "bKing can castle": True,
        "previous_move": "",
    }


def test_king_move(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/3K4/8/8/8")
    test_flags["wKing can castle"] = False

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    possible_moves.sort()
    assert possible_moves == [
        "Kd4c3",
        "Kd4c4",
        "Kd4c5",
        "Kd4d3",
        "Kd4d5",
        "Kd4e3",
        "Kd4e4",
        "Kd4e5",
    ]


def test_black_king_move(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/3k4/8/8/8")
    test_flags["color"] = "b"
    test_flags["bKing can castle"] = False

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    possible_moves.sort()
    assert possible_moves == [
        "Kd4c3",
        "Kd4c4",
        "Kd4c5",
        "Kd4d3",
        "Kd4d5",
        "Kd4e3",
        "Kd4e4",
        "Kd4e5",
    ]


def test_king_capture(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/2p1p3/3K4/3P4/8/8")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    possible_moves.sort()
    assert possible_moves == ["Kd4c3", "Kd4c4", "Kd4d5", "Kd4e3", "Kd4e4", "Kd4xc5", "Kd4xe5"]


def test_king_castle(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/8/8/R3K2R")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    assert "0-0" in possible_moves
    assert "0-0-0" in possible_moves


def test_king_cannot_castle_because_he_moved(
    test_board: Board, test_flags: dict[str, str | bool]
) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/8/8/R3K2R")
    test_flags["wKing can castle"] = False

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    assert "0-0" not in possible_moves
    assert "0-0-0" not in possible_moves


def test_king_cannot_castle_other_reasons(
    test_board: Board, test_flags: dict[str, str | bool]
) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/8/8/B3K1NR")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    assert "0-0" not in possible_moves
    assert "0-0-0" not in possible_moves


def test_king_cannot_king_castle_path_in_check(
    test_board: Board, test_flags: dict[str, str | bool]
) -> None:
    test_board.load_board_from_FEN("6r1/8/8/8/8/8/PPPPP2P/R3K2R")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    assert "0-0" not in possible_moves
    assert "0-0-0" in possible_moves

    test_board.load_board_from_FEN("5r2/8/8/8/8/8/PPPPP2P/R3K2R")
    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    assert "0-0" not in possible_moves
    assert "0-0-0" in possible_moves


def test_king_cannot_queen_castle_path_in_check(
    test_board: Board, test_flags: dict[str, str | bool]
) -> None:
    test_board.load_board_from_FEN("1r1r4/8/8/8/8/8/Pb2PPPP/R3K2R")

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    assert "0-0" in possible_moves
    assert "0-0-0" not in possible_moves


def test_black_king_castle(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    test_flags["color"] = "b"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    assert "0-0" in possible_moves
    assert "0-0-0" in possible_moves


def test_black_king_cannot_castle(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("r3k2r/ppppp2p/8/8/8/8/8/5RR1")
    test_flags["color"] = "b"

    test_position = Position(test_board.board_content, test_flags)
    possible_moves = test_position.get_valid_moves()

    assert "0-0" not in possible_moves
    assert "0-0-0" in possible_moves
