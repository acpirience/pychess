"""

Tests for piece.py

"""

from piece import Piece


def test_piece_str() -> None:
    test_piece = Piece("K", "w")
    assert f"{test_piece}" == "Kw"

    test_piece = Piece("P", "b")
    assert f"{test_piece}" == "Pb"


def test_piece_bool() -> None:
    assert not Piece()

    test_piece = Piece("N", "w")
    assert test_piece


def test_piece_eq() -> None:
    assert Piece("N", "w") == Piece("N", "w")
    assert not (Piece("N", "w") == Piece("N", "b"))
    assert not (Piece("N", "w") == "Nw")
