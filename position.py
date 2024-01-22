"""

Object used to analyse a position during a game

"""

from loguru import logger

from piece import Piece


class Position:
    def __init__(self, board: list[list[Piece]], flags: dict[str, str]) -> None:
        self.board = board
        self.flags = flags

    def get_possible_moves(self) -> list[str]:
        pieces = []

        # get all pieces of the color of which turn it is
        for line in range(8):
            for col in range(8):
                if self.board[line][col].color == self.flags["color"]:
                    pieces.append((self.board[line][col], line, col))

        for piece, line, col in pieces:
            moves = self.get_moves_for_piece(piece, line, col)
        return moves

    def get_moves_for_piece(self, piece: Piece, line: int, col: int) -> list[str]:
        moves: list[str] = []

        # Pawn
        if piece.piece == "P":
            if self.flags["color"] == "w":
                # move
                if not self.board[line - 1][col]:  # Pawn move 1 square
                    moves.append(
                        f"{Position._col_to_letter(col)}{Position._line_to_board(line -1)}"
                    )
                    if line == 6:  # if first move can move 2 squares
                        if not self.board[line - 2][col]:
                            moves.append(
                                f"{Position._col_to_letter(col)}{Position._line_to_board(line - 2)}"
                            )
                # capture
                for i in [-1, 1]:
                    if 0 <= col + i <= 7:
                        if (
                            self.board[line - 1][col + i]
                            and self.board[line - 1][col + i].color == "b"
                        ):
                            moves.append(
                                f"{Position._col_to_letter(col)}x{Position._col_to_letter(col + i)}{Position._line_to_board(line - 1)}"
                            )
                # en passant TBD

        if moves:
            logger.info(moves)
        return moves

    @staticmethod
    def _col_to_letter(col: int) -> str:
        return f"{chr(col + 97)}"

    @staticmethod
    def _line_to_board(line: int) -> int:
        return 8 - line
