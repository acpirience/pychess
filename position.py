"""

Object used to analyse a position during a game

"""


from piece import Piece


class Position:
    def __init__(self, board: list[list[Piece]], flags: dict[str, str | bool]) -> None:
        self.board = board
        self.flags = flags

    def get_possible_moves(self) -> list[str]:
        # public method used by Game object
        return self._get_possible_moves(self.board, str(self.flags["color"]))

    def king_is_in_check(self, board: list[list[Piece]], color: str) -> bool:
        coords = Position._get_king_coords(board, str(self.flags["color"]))
        if coords == "ERROR":
            return False
        return self.square_is_attacked(board, coords, color)

    def square_is_attacked(self, board: list[list[Piece]], coords: str, color: str) -> bool:
        # square can be target of attack of color opposite of "color"
        possible_targets = [
            x[-2:] for x in self._get_possible_captures(board, Position._invert_color(color))
        ]
        return coords in possible_targets

    def _get_possible_moves(
        self, board: list[list[Piece]], color: str, capture_only: bool = False
    ) -> list[str]:
        # private method used internally by Board
        pieces = []

        # get all pieces of the current color
        for line in range(8):
            for col in range(8):
                if board[line][col].color == color:
                    pieces.append((board[line][col], line, col))

        moves = []
        for piece, line, col in pieces:
            moves += self._get_moves_for_piece(board, piece, line, col, color, capture_only)

        return moves

    def _get_possible_captures(self, board: list[list[Piece]], color: str) -> list[str]:
        return self._get_possible_moves(board, color, capture_only=True)

    def _get_moves_for_piece(
        self,
        board: list[list[Piece]],
        piece: Piece,
        line: int,
        col: int,
        color: str,
        capture_only: bool = False,
    ) -> list[str]:
        moves: list[str] = []

        match piece.piece:
            case "P":  # Pawn
                moves += self._get_moves_for_pawn(board, line, col, color, capture_only)
            case "R":  # Rook
                moves += self._get_moves_for_rook(board, line, col, color)
            case "N":  # Knight
                moves += self._get_moves_for_knight(board, line, col, color)
            case "B":  # Bishop
                moves += self._get_moves_for_bishop(board, line, col, color)
            case "Q":  # Bishop
                moves += self._get_moves_for_queen(board, line, col, color)
            case "K":  # King
                moves += self._get_moves_for_king(board, line, col, color, capture_only)

        return moves

    def _get_moves_for_pawn(
        self, board: list[list[Piece]], line: int, col: int, color: str, capture_only: bool = False
    ) -> list[str]:
        PAWN_MOVE_DIRECTION = -1 if color == "w" else 1
        moves: list[str] = []
        # move
        if not capture_only:
            if not board[line + PAWN_MOVE_DIRECTION][col]:  # Pawn move 1 square
                moves.append(
                    f"{Position._xy_to_chess_coords(line, col)}"
                    f"{Position._xy_to_chess_coords(line + PAWN_MOVE_DIRECTION, col)}"
                )
                if (line == 6 and color == "w") or (line == 1 and color == "b"):
                    # if first move can move 2 squares
                    if not board[line + PAWN_MOVE_DIRECTION * 2][col]:
                        moves.append(
                            f"{Position._xy_to_chess_coords(line, col)}"
                            f"{Position._xy_to_chess_coords(line + PAWN_MOVE_DIRECTION * 2, col)}"
                        )
        # capture
        for i in [-1, 1]:
            if 0 <= col + i <= 7:
                if board[line + PAWN_MOVE_DIRECTION][col + i] and board[line + PAWN_MOVE_DIRECTION][
                    col + i
                ].color == Position._invert_color(color):
                    moves.append(
                        f"{Position._xy_to_chess_coords(line, col)}"
                        f"x{Position._xy_to_chess_coords(line + PAWN_MOVE_DIRECTION, col + i)}"
                    )
                if capture_only and not board[line + PAWN_MOVE_DIRECTION][col + i]:
                    moves.append(
                        f"{Position._xy_to_chess_coords(line, col)}"
                        f"x{Position._xy_to_chess_coords(line + PAWN_MOVE_DIRECTION, col + i)}"
                    )

        # en passant
        if (line == 3 and color == "w") or (line == 4 and color == "b"):
            # only line where pawn can capture "en passant"
            for i in [-1, 1]:
                if 0 <= col + i <= 7:
                    # previous move was a pawn moving 2 squares on left or right of pawn
                    if (
                        str(self.flags["previous_move"])[-2:]
                        == f"{Position._xy_to_chess_coords(line, col + i)}"  # end square is beside pawn
                        and len(str(self.flags["previous_move"]))
                        == 4  # pawn move is 4 length string
                        and abs(
                            int(str(self.flags["previous_move"])[-1])
                            - int(str(self.flags["previous_move"])[-3])
                        )
                        == 2  # 2 square move
                    ):
                        moves.append(
                            f"{Position._xy_to_chess_coords(line, col)}"
                            f"x{Position._xy_to_chess_coords(line + PAWN_MOVE_DIRECTION, col + i)}"
                        )

        # promotion TBD

        return moves

    def _get_moves_for_rook(
        self, board: list[list[Piece]], line: int, col: int, color: str
    ) -> list[str]:
        moves: list[str] = []
        # moves
        for move_type in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            cur_line, cur_col = line, col
            # traverse all 4 directions
            while (0 <= cur_line + move_type[0] <= 7) and (0 <= cur_col + move_type[1] <= 7):
                if not board[cur_line + move_type[0]][cur_col + move_type[1]]:
                    # empty square
                    moves.append(
                        f"R{Position._xy_to_chess_coords(line, col)}"
                        f"{Position._xy_to_chess_coords(cur_line + move_type[0], cur_col + move_type[1])}"
                    )
                else:
                    if board[cur_line + move_type[0]][
                        cur_col + move_type[1]
                    ].color == Position._invert_color(color):
                        # square contains black piece => capture
                        moves.append(
                            f"R{Position._xy_to_chess_coords(line, col)}"
                            f"x{Position._xy_to_chess_coords(cur_line + move_type[0], cur_col + move_type[1])}"
                        )
                    # square not empty, next type of move
                    break
                cur_line += move_type[0]
                cur_col += move_type[1]

        return moves

    def _get_moves_for_knight(
        self, board: list[list[Piece]], line: int, col: int, color: str
    ) -> list[str]:
        moves: list[str] = []
        # move and capture
        for move_type in [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]:
            if (0 <= line + move_type[0] <= 7) and (0 <= col + move_type[1] <= 7):
                if not board[line + move_type[0]][col + move_type[1]]:
                    moves.append(
                        f"N{Position._xy_to_chess_coords(line, col)}"
                        f"{Position._xy_to_chess_coords(line + move_type[0], col + move_type[1])}"
                    )
                elif board[line + move_type[0]][col + move_type[1]].color == Position._invert_color(
                    color
                ):
                    moves.append(
                        f"N{Position._xy_to_chess_coords(line, col)}"
                        f"x{Position._xy_to_chess_coords(line + move_type[0], col + move_type[1])}"
                    )

        return moves

    def _get_moves_for_bishop(
        self, board: list[list[Piece]], line: int, col: int, color: str
    ) -> list[str]:
        moves: list[str] = []
        # moves
        for move_type in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            cur_line, cur_col = line, col
            # traverse all 4 directions
            while (0 <= cur_line + move_type[0] <= 7) and (0 <= cur_col + move_type[1] <= 7):
                if not board[cur_line + move_type[0]][cur_col + move_type[1]]:
                    # empty square
                    moves.append(
                        f"B{Position._xy_to_chess_coords(line, col)}"
                        f"{Position._xy_to_chess_coords(cur_line + move_type[0], cur_col + move_type[1])}"
                    )
                else:
                    if board[cur_line + move_type[0]][
                        cur_col + move_type[1]
                    ].color == Position._invert_color(color):
                        # square contains opposite color piece => capture
                        moves.append(
                            f"B{Position._xy_to_chess_coords(line, col)}"
                            f"x{Position._xy_to_chess_coords(cur_line + move_type[0], cur_col + move_type[1])}"
                        )
                    # square not empty, next type of move
                    break
                cur_line += move_type[0]
                cur_col += move_type[1]

        return moves

    def _get_moves_for_queen(
        self, board: list[list[Piece]], line: int, col: int, color: str
    ) -> list[str]:
        moves: list[str] = []
        # moves
        for move_type in [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            cur_line, cur_col = line, col
            # traverse all 8 directions
            while (0 <= cur_line + move_type[0] <= 7) and (0 <= cur_col + move_type[1] <= 7):
                if not board[cur_line + move_type[0]][cur_col + move_type[1]]:
                    # empty square
                    moves.append(
                        f"Q{Position._xy_to_chess_coords(line, col)}"
                        f"{Position._xy_to_chess_coords(cur_line + move_type[0], cur_col + move_type[1])}"
                    )
                else:
                    if board[cur_line + move_type[0]][
                        cur_col + move_type[1]
                    ].color == Position._invert_color(color):
                        # square contains black piece => capture
                        moves.append(
                            f"Q{Position._xy_to_chess_coords(line, col)}"
                            f"x{Position._xy_to_chess_coords(cur_line + move_type[0], cur_col + move_type[1])}"
                        )
                    # square not empty, next type of move
                    break
                cur_line += move_type[0]
                cur_col += move_type[1]

        return moves

    def _get_moves_for_king(
        self, board: list[list[Piece]], line: int, col: int, color: str, capture_only: bool = False
    ) -> list[str]:
        moves: list[str] = []
        # move and capture
        for move_type in [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1), (0, -1), (0, 1)]:
            if (0 <= line + move_type[0] <= 7) and (0 <= col + move_type[1] <= 7):
                if not board[line + move_type[0]][col + move_type[1]]:
                    moves.append(
                        f"K{Position._xy_to_chess_coords(line, col)}"
                        f"{Position._xy_to_chess_coords(line + move_type[0], col + move_type[1])}"
                    )
                elif board[line + move_type[0]][col + move_type[1]].color == Position._invert_color(
                    color
                ):
                    moves.append(
                        f"K{Position._xy_to_chess_coords(line, col)}"
                        f"x{Position._xy_to_chess_coords(line + move_type[0], col + move_type[1])}"
                    )
        # castle
        if capture_only or not self.flags[f"{self.flags['color']}King can castle"]:
            return moves

        if (line == 7 and col == 4 and color == "w") or (line == 0 and col == 4 and color == "b"):
            if (
                not board[line][col + 1]
                and not board[line][col + 2]
                and board[line][col + 3] == Piece("R", color)
            ):
                if not self.square_is_attacked(
                    board, Position._xy_to_chess_coords(line, col + 1), color
                ) and not self.square_is_attacked(
                    board, Position._xy_to_chess_coords(line, col + 2), color
                ):
                    moves.append("0-0")
            if (
                not board[line][col - 1]
                and not board[line][col - 2]
                and not board[line][col - 3]
                and board[line][col - 4] == Piece("R", color)
            ):
                if (
                    not self.square_is_attacked(
                        board, Position._xy_to_chess_coords(line, col - 1), color
                    )
                    and not self.square_is_attacked(
                        board, Position._xy_to_chess_coords(line, col - 2), color
                    )
                    and not self.square_is_attacked(
                        board, Position._xy_to_chess_coords(line, col - 2), color
                    )
                ):
                    moves.append("0-0-0")

        return moves

    @staticmethod
    def _invert_coords(coords: str) -> str:
        return f"{coords[0]}{9 - int(str(coords[1]))}"

    @staticmethod
    def _invert_color(color: str) -> str:
        if color == "w":
            return "b"
        return "w"

    @staticmethod
    def _col_to_letter(col: int) -> str:
        return f"{chr(col + 97)}"

    @staticmethod
    def _line_to_board(line: int) -> int:
        return 8 - line

    @staticmethod
    def _xy_to_chess_coords(line: int, col: int) -> str:
        return f"{Position._col_to_letter(col)}{Position._line_to_board(line)}"

    @staticmethod
    def _get_king_coords(board: list[list[Piece]], color: str) -> str:
        for line in range(8):
            for col in range(8):
                if board[line][col] == Piece("K", color):
                    return Position._xy_to_chess_coords(line, col)
        return "ERROR"  # should never be reached
