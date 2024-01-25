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

        moves = []
        for piece, line, col in pieces:
            moves += self.get_moves_for_piece(piece, line, col)

        logger.info(moves)
        return moves

    def get_moves_for_piece(self, piece: Piece, line: int, col: int) -> list[str]:
        moves: list[str] = []

        match piece.piece:
            case "P":  # Pawn
                moves += self._get_moves_for_pawn(line, col)
            case "R":  # Rook
                moves += self._get_moves_for_rook(line, col)
            case "N":  # Knight
                moves += self._get_moves_for_knight(line, col)
            case _:
                logger.error(f"{piece.piece} Not implemented yet")

        return moves

    def _get_moves_for_pawn(self, line: int, col: int) -> list[str]:
        moves: list[str] = []
        # move
        if not self.board[line - 1][col]:  # Pawn move 1 square
            moves.append(f"{Position._col_to_letter(col)}{self._line_to_board(line - 1)}")
            if line == 6:  # if first move can move 2 squares
                if not self.board[line - 2][col]:
                    moves.append(f"{Position._col_to_letter(col)}{self._line_to_board(line - 2)}")
        # capture
        for i in [-1, 1]:
            if 0 <= col + i <= 7:
                if self.board[line - 1][col + i] and self.board[line - 1][col + i].color == "b":
                    moves.append(
                        f"{Position._col_to_letter(col)}x{Position._col_to_letter(col + i)}{self._line_to_board(line - 1)}"
                    )
        # en passant
        if line == 3:  # only line where pawn can capture "en passant"
            for i in [-1, 1]:
                if 0 <= col + i <= 7:
                    # previous move was a pawn moving 2 squares on left or right of pawn
                    if (
                        self.flags["previous_move"]
                        == f"{Position._col_to_letter(col + i)}{self._line_to_board(line)}"
                    ):
                        moves.append(
                            f"{Position._col_to_letter(col)}x{Position._col_to_letter(col + i)}{self._line_to_board(line - 1)}"
                        )

        return moves

    def _get_moves_for_rook(self, line: int, col: int) -> list[str]:
        moves: list[str] = []
        # moves
        for move_type in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            cur_line, cur_col = line, col
            # traverse all 4 directions
            while (0 <= cur_line + move_type[0] <= 7) and (0 <= cur_col + move_type[1] <= 7):
                if not self.board[cur_line + move_type[0]][cur_col + move_type[1]]:
                    # empty square
                    moves.append(
                        f"R{Position._col_to_letter(cur_col + move_type[1])}{self._line_to_board(cur_line + move_type[0])}"
                    )
                else:
                    if self.board[cur_line + move_type[0]][cur_col + move_type[1]].color == "b":
                        # square contains black piece => capture
                        moves.append(
                            f"Rx{Position._col_to_letter(cur_col + move_type[1])}{self._line_to_board(cur_line + move_type[0])}"
                        )
                    # square not empty, next type of move
                    break
                cur_line += move_type[0]
                cur_col += move_type[1]

        return moves

    def _get_moves_for_knight(self, line: int, col: int) -> list[str]:
        moves: list[str] = []
        # move and capture
        for move_type in [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]:
            if (0 <= line + move_type[0] <= 7) and (0 <= col + move_type[1] <= 7):
                if not self.board[line + move_type[0]][col + move_type[1]]:
                    moves.append(
                        f"N{Position._col_to_letter(col + move_type[1])}{self._line_to_board(line + move_type[0])}"
                    )
                elif self.board[line + move_type[0]][col + move_type[1]].color == "b":
                    moves.append(
                        f"Nx{Position._col_to_letter(col + move_type[1])}{self._line_to_board(line + move_type[0])}"
                    )

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

    @staticmethod
    def _invert_color(color: str) -> str:
        if color == "w":
            return "b"
        return "w"

    @staticmethod
    def _col_to_letter(col: int) -> str:
        return f"{chr(col + 97)}"
