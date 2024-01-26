"""

class containing a chess piece

"""


class Piece:
    def __init__(self, piece: str = "", color: str = "") -> None:
        self.piece = piece
        self.color = color

    def __str__(self) -> str:
        return f"{self.piece}{self.color}"

    def __bool__(self) -> bool:
        return bool(self.__str__())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Piece):
            return False
        return (self.piece == other.piece) and (self.color == other.color)
