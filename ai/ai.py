"""

basic ai class

"""

import threading
from random import randint

from move import Move
from position import Position


class Ai:
    def __init__(self, position: Position, color: str):
        self.position = position
        self.color = color
        self.get_next_move_finished = False
        self.move: Move

        # create thread on method get_next_move, the game object will
        # use get_next_move_finished to detect end of thread
        thread = threading.Thread(target=self.get_next_move, args=())
        thread.daemon = True
        thread.start()

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
