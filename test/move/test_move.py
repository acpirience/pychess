"""

Tests for move.py

"""

from move import Move


def test_move_str() -> None:
    test_move = Move((1, 0), (2, 0), "a2a3")
    assert f"{test_move}" == "a2a3"
