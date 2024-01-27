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
        return self.square_is_in_check(board, coords, color)

    def square_is_in_check(self, board: list[list[Piece]], coords: str, color: str) -> bool:
        opponent_board = board
        if color == "b":
            coords = Position._invert_coords(coords)
        opponent_moves = self._get_possible_moves(
            opponent_board, Position._invert_color(color), add_pawn_capture=True
        )
        opponent_targets = [x[-2:] for x in opponent_moves]
        if coords in opponent_targets:
            return True
        return False

    def _get_possible_moves(
        self, board: list[list[Piece]], color: str, add_pawn_capture: bool = False
    ) -> list[str]:
        # private method used internally by Board
        if color == "b":
            board = Position._invert_board(board)

        pieces = []

        # get all pieces white color
        for line in range(8):
            for col in range(8):
                if board[line][col].color == "w":
                    pieces.append((board[line][col], line, col))

        moves = []
        for piece, line, col in pieces:
            moves += self._get_moves_for_piece(board, piece, line, col, color, add_pawn_capture)

        # logger.info(moves)
        return moves

    def _get_moves_for_piece(
        self,
        board: list[list[Piece]],
        piece: Piece,
        line: int,
        col: int,
        color: str,
        add_pawn_capture: bool,
    ) -> list[str]:
        moves: list[str] = []

        match piece.piece:
            case "P":  # Pawn
                moves += self._get_moves_for_pawn(board, line, col, color, add_pawn_capture)
            case "R":  # Rook
                moves += self._get_moves_for_rook(board, line, col, color)
            case "N":  # Knight
                moves += self._get_moves_for_knight(board, line, col, color)
            case "B":  # Bishop
                moves += self._get_moves_for_bishop(board, line, col, color)
            case "Q":  # Bishop
                moves += self._get_moves_for_queen(board, line, col, color)
            case "K":  # King
                moves += self._get_moves_for_king(board, line, col, color)

        return moves

    def _get_moves_for_pawn(
        self, board: list[list[Piece]], line: int, col: int, color: str, add_pawn_capture: bool
    ) -> list[str]:
        moves: list[str] = []
        # move
        if not board[line - 1][col]:  # Pawn move 1 square
            moves.append(
                f"{Position._xy_to_chess_coords(line, col, color)}"
                f"{Position._xy_to_chess_coords(line - 1, col, color)}"
            )
            if line == 6:  # if first move can move 2 squares
                if not board[line - 2][col]:
                    moves.append(
                        f"{Position._xy_to_chess_coords(line, col, color)}"
                        f"{Position._xy_to_chess_coords(line -2, col, color)}"
                    )
        # capture
        for i in [-1, 1]:
            if 0 <= col + i <= 7:
                if board[line - 1][col + i] and board[line - 1][col + i].color == "b":
                    moves.append(
                        f"{Position._xy_to_chess_coords(line, col, color)}"
                        f"x{Position._xy_to_chess_coords(line - 1, col + i, color)}"
                    )
                if add_pawn_capture:  # special case for pawn used by square_is_in_check
                    if not board[line - 1][col + i]:
                        moves.append(
                            f"{Position._xy_to_chess_coords(line, col, color)}"
                            f"x{Position._xy_to_chess_coords(line - 1, col + i, color)}"
                        )

        # en passant
        if line == 3:  # only line where pawn can capture "en passant"
            for i in [-1, 1]:
                if 0 <= col + i <= 7:
                    # previous move was a pawn moving 2 squares on left or right of pawn
                    if (
                        str(self.flags["previous_move"])[-2:]
                        == f"{Position._xy_to_chess_coords(line, col + i, color)}"
                    ):
                        moves.append(
                            f"{Position._xy_to_chess_coords(line, col, color)}"
                            f"x{Position._xy_to_chess_coords(line - 1, col + i, color)}"
                        )

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
                        f"R{Position._xy_to_chess_coords(line, col, color)}"
                        f"{Position._xy_to_chess_coords(cur_line + move_type[0], cur_col + move_type[1], color)}"
                    )
                else:
                    if board[cur_line + move_type[0]][cur_col + move_type[1]].color == "b":
                        # square contains black piece => capture
                        moves.append(
                            f"R{Position._xy_to_chess_coords(line, col, color)}"
                            f"x{Position._xy_to_chess_coords(cur_line + move_type[0], cur_col + move_type[1], color)}"
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
                        f"N{Position._xy_to_chess_coords(line, col, color)}"
                        f"{Position._xy_to_chess_coords(line + move_type[0], col + move_type[1], color)}"
                    )
                elif board[line + move_type[0]][col + move_type[1]].color == "b":
                    moves.append(
                        f"N{Position._xy_to_chess_coords(line, col, color)}"
                        f"x{Position._xy_to_chess_coords(line + move_type[0], col + move_type[1], color)}"
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
                        f"B{Position._xy_to_chess_coords(line, col, color)}"
                        f"{Position._xy_to_chess_coords(cur_line + move_type[0], cur_col + move_type[1], color)}"
                    )
                else:
                    if board[cur_line + move_type[0]][cur_col + move_type[1]].color == "b":
                        # square contains black piece => capture
                        moves.append(
                            f"B{Position._xy_to_chess_coords(line, col, color)}"
                            f"x{Position._xy_to_chess_coords(cur_line + move_type[0], cur_col + move_type[1], color)}"
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
                        f"Q{Position._xy_to_chess_coords(line, col, color)}"
                        f"{Position._xy_to_chess_coords(cur_line + move_type[0], cur_col + move_type[1], color)}"
                    )
                else:
                    if board[cur_line + move_type[0]][cur_col + move_type[1]].color == "b":
                        # square contains black piece => capture
                        moves.append(
                            f"Q{Position._xy_to_chess_coords(line, col, color)}"
                            f"x{Position._xy_to_chess_coords(cur_line + move_type[0], cur_col + move_type[1], color)}"
                        )
                    # square not empty, next type of move
                    break
                cur_line += move_type[0]
                cur_col += move_type[1]

        return moves

    def _get_moves_for_king(
        self, board: list[list[Piece]], line: int, col: int, color: str
    ) -> list[str]:
        moves: list[str] = []
        # move and capture
        for move_type in [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1), (0, -1), (0, 1)]:
            if (0 <= line + move_type[0] <= 7) and (0 <= col + move_type[1] <= 7):
                if not board[line + move_type[0]][col + move_type[1]]:
                    moves.append(
                        f"K{Position._xy_to_chess_coords(line, col, color)}"
                        f"{Position._xy_to_chess_coords(line + move_type[0], col + move_type[1], color)}"
                    )
                elif board[line + move_type[0]][col + move_type[1]].color == "b":
                    moves.append(
                        f"K{Position._xy_to_chess_coords(line, col, color)}"
                        f"x{Position._xy_to_chess_coords(line + move_type[0], col + move_type[1], color)}"
                    )
        # castle
        if self.flags[f"{self.flags['color']}King can castle"] and line == 7 and col == 4:
            if (
                not board[line][col + 1]
                and not board[line][col + 2]
                and board[line][col + 3] == Piece("R", "w")
            ):
                if not self.square_is_in_check(board, "f1", "w") and not self.square_is_in_check(
                    board, "g1", "w"
                ):
                    moves.append("0-0")
            if (
                not board[line][col - 1]
                and not board[line][col - 2]
                and not board[line][col - 3]
                and board[line][col - 4] == Piece("R", "w")
            ):
                if (
                    not self.square_is_in_check(board, "d1", "w")
                    and not self.square_is_in_check(board, "c1", "w")
                    and not self.square_is_in_check(board, "b1", "w")
                ):
                    moves.append("0-0-0")

        return moves

    @staticmethod
    def _invert_board(board: list[list[Piece]]) -> list[list[Piece]]:
        new_board = []
        for line in reversed(board):
            new_line = []
            for piece in line:
                if piece:
                    new_line.append(Piece(piece.piece, Position._invert_color(piece.color)))
                else:
                    new_line.append(Piece())
            new_board.append(new_line)

        return new_board

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
    def _line_to_board(line: int, color: str) -> int:
        if color == "w":
            return 8 - line
        return line + 1

    @staticmethod
    def _xy_to_chess_coords(line: int, col: int, color: str) -> str:
        return f"{Position._col_to_letter(col)}{Position._line_to_board(line, color)}"

    @staticmethod
    def _get_king_coords(board: list[list[Piece]], color: str) -> str:
        for line in range(8):
            for col in range(8):
                if board[line][col] == Piece("K", color):
                    return Position._xy_to_chess_coords(line, col, color)
        return "ERROR"  # should never be reached
