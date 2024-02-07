"""

Tests for position.py - is_in_check

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


def test_king_in_check_with_pawn(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/8/5p2/RNBQKBNR")

    test_position = Position(test_board.board_content, test_flags)
    assert test_position.king_is_in_check(test_board.board_content)


def test_king_in_check_with_rook(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("4r3/8/8/8/8/8/8/RNBQKBNR")

    test_position = Position(test_board.board_content, test_flags)
    assert test_position.king_is_in_check(test_board.board_content)


def test_king_in_check_with_knight(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/8/6n1/RNBQKBNR")

    test_position = Position(test_board.board_content, test_flags)
    assert test_position.king_is_in_check(test_board.board_content)


def test_king_in_check_with_bishop(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/b7/8/8/8/RNBQKBNR")

    test_position = Position(test_board.board_content, test_flags)
    assert test_position.king_is_in_check(test_board.board_content)


def test_king_in_check_with_queen(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/4q3/8/8/8/RNBQKBNR")

    test_position = Position(test_board.board_content, test_flags)
    assert test_position.king_is_in_check(test_board.board_content)


def test_black_king_in_check_by_knight(
    test_board: Board, test_flags: dict[str, str | bool]
) -> None:
    test_board.load_board_from_FEN("rnbqkbnr/pppppppp/3N4/8/8/8/PPPPPPPP/R1BQKBNR")
    test_flags["color"] = "b"

    test_position = Position(test_board.board_content, test_flags)
    assert test_position.king_is_in_check(test_board.board_content)


def test_black_king_in_check_by_rook(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    test_board.load_board_from_FEN("8/8/8/8/8/8/8/k1R4K")
    test_flags["color"] = "b"

    test_position = Position(test_board.board_content, test_flags)
    assert test_position.king_is_in_check(test_board.board_content)


def test_no_chess_if_no_king(test_board: Board, test_flags: dict[str, str | bool]) -> None:
    # avoid crashing if no king on the board for tests
    test_board.load_board_from_FEN("8/8/8/8/8/8/8/8")

    test_position = Position(test_board.board_content, test_flags)
    assert not test_position.king_is_in_check(test_board.board_content)
