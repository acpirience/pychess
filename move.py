"""

class containing a chess move (square from / square to / chess move name

"""


class Move:
    def __init__(
        self, square_from: tuple[int, int], square_to: tuple[int, int], chess_move: str
    ) -> None:
        self.square_from = square_from
        self.square_to = square_to
        self.chess_move = chess_move

    def __str__(self) -> str:
        return self.chess_move
