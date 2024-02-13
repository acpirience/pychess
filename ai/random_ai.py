"""

Random ai class; all moves are at random

"""

from random import randint

from ai.ai import Ai
from position import Position


class Random_Ai(Ai):
    def __init__(self, position: Position, color: str):
        super().__init__(position, color)

    def get_next_move(self) -> None:
        # to be implemented by each AI
        # example of a totally random AI

        valid_move = self.position.valid_moves

        if not valid_move:
            return

        self.move = valid_move[randint(0, len(valid_move) - 1)]
        # promotion special case => always choose queen
        if self.move.chess_move[0].islower():
            if (self.color == "w" and self.move.square_to[0] == 0) or (
                self.color == "b" and self.move.square_to[0] == 7
            ):
                self.move.chess_move += "Q"

        self.get_next_move_finished = True
