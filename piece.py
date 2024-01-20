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
