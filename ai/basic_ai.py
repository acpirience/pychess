"""

basic ai class; evaluate board and go with move giving the biggest note

"""

from random import randint

from ai.ai import Ai
from move import Move
from piece import Piece
from position import Position

PIECE_VALUE = {"P": 10, "N": 30, "B": 30, "R": 50, "Q": 90, "K": 900}


class Basic_Ai(Ai):
    def __init__(self, position: Position, color: str):
        super().__init__(position, color)

    def get_next_move(self) -> None:
        # to be implemented by each AI
        # example of a totally random AI

        valid_move = self.position.valid_moves

        if not valid_move:
            return

        self.move = self.get_get_best_move()

        # promotion special case => always choose queen
        if self.move.chess_move[0].islower():
            if (self.color == "w" and self.move.square_to[0] == 0) or (
                self.color == "b" and self.move.square_to[0] == 7
            ):
                self.move.chess_move += "Q"

        self.get_next_move_finished = True

    def get_get_best_move(self) -> Move:
        move_scores: list[tuple[Move, int]] = []

        max_score = -9999999999
        for move in self.position.valid_moves:
            board = self.position.get_board_after_move(move, self.position.board, self.color)
            score = self.evaluate_board(board, self.color)
            if score > max_score:
                max_score = score
            move_scores.append((move, score))

        chosen_moves = [x[0] for x in move_scores if x[1] == max_score]

        return chosen_moves[randint(0, len(chosen_moves) - 1)]

    def evaluate_board(self, board: list[list[Piece]], color: str) -> int:
        score = 0
        for line in range(8):
            for col in range(8):
                if board[line][col]:
                    value = PIECE_VALUE[board[line][col].piece]
                    if board[line][col].color == "w":
                        score += value
                    else:
                        score -= value

        if color == "b":
            score = -score
        return score
