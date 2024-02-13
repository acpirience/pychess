"""

ai class model

"""

import threading

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
        pass
