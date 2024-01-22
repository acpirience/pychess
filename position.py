"""

Object used to analyse a position during a game

"""

from loguru import logger

from piece import Piece


class Position:
    def __init__(self, board: list[list[Piece]], flags: dict[str, str]) -> None:
        self.board = board
        self.flags = flags

        if self.flags["color"] == "b":
            self._invert_board()

    def get_possible_moves(self) -> list[str]:
        pieces = []

        # get all pieces white color
        for line in range(8):
            for col in range(8):
                if self.board[line][col].color == "w":
                    pieces.append((self.board[line][col], line, col))
                    logger.info(f"{self.board[line][col]}, {line} {col}")

        for piece, line, col in pieces:
            moves = self.get_moves_for_piece(piece, line, col)
        return moves

    def get_moves_for_piece(self, piece: Piece, line: int, col: int) -> list[str]:
        moves: list[str] = []

        # Pawn
        if piece.piece == "P":
            # move
            if not self.board[line - 1][col]:  # Pawn move 1 square
                moves.append(f"{Position._col_to_letter(col)}{self._line_to_board(line -1)}")
                if line == 6:  # if first move can move 2 squares
                    if not self.board[line - 2][col]:
                        moves.append(
                            f"{Position._col_to_letter(col)}{self._line_to_board(line - 2)}"
                        )
            # capture
            for i in [-1, 1]:
                if 0 <= col + i <= 7:
                    if self.board[line - 1][col + i] and self.board[line - 1][col + i].color == "b":
                        moves.append(
                            f"{Position._col_to_letter(col)}x{Position._col_to_letter(col + i)}{self._line_to_board(line - 1)}"
                        )
            # en passant TBD

        if moves:
            logger.info(moves)
        return moves

    def _line_to_board(self, line: int) -> int:
        if self.flags["color"] == "w":
            return 8 - line
        return line + 1

    def _invert_board(self) -> None:
        new_board = []
        for line in reversed(self.board):
            new_line = []
            for piece in line:
                if piece:
                    new_line.append(Piece(piece.piece, Position._invert_color(piece.color)))
                else:
                    new_line.append(Piece())
            new_board.append(new_line)

        self.board = new_board
        for x in range(8):
            logger.info(
                f"{self.board[x][0]} {self.board[x][1]} {self.board[x][2]} {self.board[x][3]} {self.board[x][4]} {self.board[x][5]} {self.board[x][6]} {self.board[x][7]}"
            )

    @staticmethod
    def _invert_color(color: str) -> str:
        if color == "w":
            return "b"
        return "w"

    @staticmethod
    def _col_to_letter(col: int) -> str:
        return f"{chr(col + 97)}"
