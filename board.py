"""

class responsible to draw the chess board in its current state

"""

import glob
import os

import pygame

from config import FONT_DIR, IMG_DIR
from piece import Piece

COLOR_SCHEME_LIST = {
    "BLACK": ["#D6D7D4", "#211E24", "#000000"],
    "WOOD": ["#F0D1A1", "#9F4A25", "#861C00"],
    "GREEN": ["#F0D1A1", "#537C49", "#234C19"],
}

COLOR_VALID_MOVE = "#26852A"

SQUARE_SIZE = 100
BORDER_SIZE = 25
BOARD_SIZE = 8 * SQUARE_SIZE

NULL_COORDS = (99, 99)
DEBUG = True


class Board:
    def __init__(
        self,
        color_scheme: str = "BLACK",
    ) -> None:
        self.color_scheme = color_scheme
        self.board_content: list[list[Piece]] = [[] for _ in range(8)]
        self.asset_loaded = False

        # Mouse
        self.mouse_coords: tuple[int, int] = (0, 0)
        self.mouse_clicked: dict[str, bool]
        self.drag = False
        self.drag_from: tuple[int, int] = NULL_COORDS  # forbidden value to keep mypy happy
        self.drag_piece = Piece()
        self.move_done = False

        self.move_map: dict[tuple[int, int], list[tuple[int, int]]] = {}

    def _load_assets(self) -> None:
        # load assets used by the object

        # fonts
        # https://www.dafont.com/fr/coolvetica.font
        self.font_board_marks = pygame.font.Font(os.path.join(FONT_DIR, "coolvetica rg.otf"), 16)

        # Images : chess pieces
        # https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces
        self.piece_list = {}
        png_list = [
            x.removeprefix(IMG_DIR + os.sep).removesuffix(".png")
            for x in glob.glob(os.path.join(IMG_DIR, "*.png"))
        ]
        for piece in png_list:
            self.piece_list[piece] = pygame.image.load(os.path.join(IMG_DIR, f"{piece}.png"))

    def update(self) -> None:
        # Shall we drag ?
        if self.mouse_clicked["BUTTONDOWN"] and not self.drag:
            coords = self.mouse_to_grid()
            if coords and coords in self.move_map:
                self.drag_piece = self.board_content[coords[0]][coords[1]]
                if self.drag_piece:
                    self.drag = True
                    self.drag_from = coords
            else:
                self.mouse_clicked["BUTTONDOWN"] = False

        # Shall we drop ?
        if not self.mouse_clicked["BUTTONDOWN"] and self.drag:
            coords = self.mouse_to_grid()
            if coords and coords in self.move_map[self.drag_from]:
                # valid move => drop
                self.do_move(self.drag_from, coords)
                pass
            else:
                # invalid move => un drag
                self.drag_piece = Piece()
                self.drag = False
                self.drag_from = NULL_COORDS

    def render(self, game_canvas: pygame.Surface) -> None:
        # render board on screen

        # if assets not loaded, load them (to avoid an error in pytest)
        if not self.asset_loaded:
            self._load_assets()
            self.asset_loaded = True
        self.square_colors = COLOR_SCHEME_LIST[self.color_scheme]
        self._render_back(game_canvas)
        self._render_board(game_canvas)
        self._render_marks(game_canvas)
        self._render_pieces(game_canvas)
        self._render_mouse_over(game_canvas)
        if DEBUG:
            self._render_debug(game_canvas)

    def _render_debug(self, game_canvas: pygame.Surface) -> None:
        coords = self.mouse_to_grid()
        debug_string = f"{self.mouse_coords} {coords} "
        if not coords == NULL_COORDS:
            debug_string += str(self.board_content[coords[0]][coords[1]])

        game_canvas.blit(
            self.font_board_marks.render(
                debug_string,
                True,
                pygame.Color("White"),
            ),
            (BOARD_SIZE + BORDER_SIZE * 2, BOARD_SIZE),
        )

        for line in range(8):
            board = f"line {line}: "
            for col in range(8):
                if self.board_content[line][col]:
                    board += str(self.board_content[line][col]) + " "
                else:
                    board += "   "
            game_canvas.blit(
                self.font_board_marks.render(
                    board,
                    True,
                    pygame.Color("White"),
                ),
                (BOARD_SIZE + BORDER_SIZE * 2, BORDER_SIZE * 5 + BORDER_SIZE * line),
            )

    def _render_board(self, game_canvas: pygame.Surface) -> None:
        for x in range(8):
            for y in range(8):
                square = pygame.Rect(
                    (
                        BORDER_SIZE + (x % 8) * SQUARE_SIZE,
                        BORDER_SIZE + (y % 8) * SQUARE_SIZE,
                    ),
                    (SQUARE_SIZE, SQUARE_SIZE),
                )

                pygame.draw.rect(game_canvas, self.square_colors[(x + y) % 2], square)

    def _render_back(self, game_canvas: pygame.Surface) -> None:
        # render back of board
        back_length = (BORDER_SIZE * 2) + (SQUARE_SIZE * 8)
        back = pygame.Rect((0, 0), (back_length, back_length))
        pygame.draw.rect(game_canvas, self.square_colors[2], back)

    def _render_marks(self, game_canvas: pygame.Surface) -> None:
        # render board marks (coordinates of squares) on screen
        numbers = [str(x + 1) for x in reversed(range(8))]
        letters = [chr(x + 65) for x in range(8)]

        for pos, letter in enumerate(letters):
            text, text_rect = Board.center_text(
                letter,
                BORDER_SIZE + (SQUARE_SIZE / 2) + (SQUARE_SIZE * pos),
                BORDER_SIZE / 2,
                self.square_colors[0],
                self.font_board_marks,
            )
            game_canvas.blit(pygame.transform.rotate(text, 180), text_rect)
            text, text_rect = Board.center_text(
                letter,
                BORDER_SIZE + (SQUARE_SIZE / 2) + (SQUARE_SIZE * pos),
                (BORDER_SIZE * 1.5) + (SQUARE_SIZE * 8),
                self.square_colors[0],
                self.font_board_marks,
            )
            game_canvas.blit(text, text_rect)

        for pos, number in enumerate(numbers):
            text, text_rect = Board.center_text(
                number,
                BORDER_SIZE / 2,
                BORDER_SIZE + (SQUARE_SIZE / 2) + (SQUARE_SIZE * pos),
                self.square_colors[0],
                self.font_board_marks,
            )
            game_canvas.blit(text, text_rect)
            text, text_rect = Board.center_text(
                number,
                (BORDER_SIZE * 1.5) + (SQUARE_SIZE * 8),
                BORDER_SIZE + (SQUARE_SIZE / 2) + (SQUARE_SIZE * pos),
                self.square_colors[0],
                self.font_board_marks,
            )
            game_canvas.blit(pygame.transform.rotate(text, 180), text_rect)

    def _render_mouse_over(self, game_canvas: pygame.Surface) -> None:
        coords = self.mouse_to_grid()
        if coords:
            line, col = coords
            # lines and targets except dragged piece
            if (line, col) in self.move_map and not self.drag:
                for target_line, target_col in self.move_map[(line, col)]:
                    center_start = (
                        BORDER_SIZE
                        + SQUARE_SIZE / 2
                        + col * SQUARE_SIZE
                        + BORDER_SIZE * Board.sign(target_col - col),
                        BORDER_SIZE
                        + SQUARE_SIZE / 2
                        + line * SQUARE_SIZE
                        + BORDER_SIZE * Board.sign(target_line - line),
                    )
                    center_end = (
                        BORDER_SIZE + SQUARE_SIZE / 2 + target_col * SQUARE_SIZE,
                        BORDER_SIZE + SQUARE_SIZE / 2 + target_line * SQUARE_SIZE,
                    )
                    self._render_line(game_canvas, center_start, center_end)

                for target_line, target_col in self.move_map[(line, col)]:
                    center_end = (
                        BORDER_SIZE + SQUARE_SIZE / 2 + target_col * SQUARE_SIZE,
                        BORDER_SIZE + SQUARE_SIZE / 2 + target_line * SQUARE_SIZE,
                    )
                    self._render_move(game_canvas, center_end)

            # lines and targets for dragged piece
            if self.drag:
                line, col = self.drag_from
                for target_line, target_col in self.move_map[line, col]:
                    center_start = (
                        BORDER_SIZE
                        + SQUARE_SIZE / 2
                        + col * SQUARE_SIZE
                        + BORDER_SIZE * Board.sign(target_col - col),
                        BORDER_SIZE
                        + SQUARE_SIZE / 2
                        + line * SQUARE_SIZE
                        + BORDER_SIZE * Board.sign(target_line - line),
                    )
                    center_end = (
                        BORDER_SIZE + SQUARE_SIZE / 2 + target_col * SQUARE_SIZE,
                        BORDER_SIZE + SQUARE_SIZE / 2 + target_line * SQUARE_SIZE,
                    )
                    self._render_line(game_canvas, center_start, center_end)

                for target_line, target_col in self.move_map[(line, col)]:
                    center_end = (
                        BORDER_SIZE + SQUARE_SIZE / 2 + target_col * SQUARE_SIZE,
                        BORDER_SIZE + SQUARE_SIZE / 2 + target_line * SQUARE_SIZE,
                    )
                    self._render_move(game_canvas, center_end)

            # square highlight
            line, col = coords
            highlight_color = pygame.Color("White")
            if (
                self.drag
                and coords not in self.move_map[self.drag_from]
                and coords != self.drag_from
            ):
                highlight_color = pygame.Color("Red")

            square = pygame.Rect(
                (
                    BORDER_SIZE + (col % 8) * SQUARE_SIZE,
                    BORDER_SIZE + (line % 8) * SQUARE_SIZE,
                ),
                (SQUARE_SIZE, SQUARE_SIZE),
            )
            pygame.draw.rect(game_canvas, highlight_color, square, 5, 5)

    def _render_line(
        self, game_canvas: pygame.Surface, start: tuple[float, float], end: tuple[float, float]
    ) -> None:
        pygame.draw.line(game_canvas, pygame.Color("Black"), start, end, 1)

    def _render_move(self, game_canvas: pygame.Surface, end: tuple[float, float]) -> None:
        pygame.draw.circle(game_canvas, pygame.Color("Black"), end, 10)
        pygame.draw.circle(game_canvas, pygame.Color(COLOR_VALID_MOVE), end, 8)

    def _render_pieces(self, game_canvas: pygame.Surface) -> None:
        # render chess pieces on screen
        cur_line = 0
        for line in self.board_content:
            cur_col = 0
            while cur_col < 8:
                if line[cur_col]:
                    if not (
                        self.drag_from != NULL_COORDS and (cur_line, cur_col) == self.drag_from
                    ):
                        game_canvas.blit(
                            self.piece_list[f"{line[cur_col]}"],
                            (
                                BORDER_SIZE + (SQUARE_SIZE * cur_col),
                                BORDER_SIZE + (SQUARE_SIZE * cur_line),
                            ),
                        )
                cur_col += 1
            cur_line += 1

        if not self.drag_from == NULL_COORDS:
            game_canvas.blit(
                self.piece_list[f"{self.board_content[self.drag_from[0]][self.drag_from[1]]}"],
                (
                    self.mouse_coords[0] - SQUARE_SIZE / 2,
                    self.mouse_coords[1] - SQUARE_SIZE / 2,
                ),
            )

    def load_board_from_FEN(self, fen_string: str) -> None:
        # load board content from a FEN string
        # https://www.chess.com/terms/fen-chess
        cur_board_line = 0
        self.board_content = [[] for _ in range(8)]
        for line in fen_string.split("/"):
            for x in line:
                if x.isdigit():
                    for _ in range(int(x)):
                        self.board_content[cur_board_line].append(Piece())
                else:
                    self.board_content[cur_board_line].append(
                        Piece(x.upper(), "b" if x.islower() else "w")
                    )
            cur_board_line += 1

    def mouse_to_grid(self) -> tuple[int, int]:
        if not (
            (BORDER_SIZE < self.mouse_coords[0] < BORDER_SIZE + BOARD_SIZE)
            and (BORDER_SIZE < self.mouse_coords[1] < BORDER_SIZE + BOARD_SIZE)
        ):
            return NULL_COORDS
        return (self.mouse_coords[1] - BORDER_SIZE) // SQUARE_SIZE, (
            self.mouse_coords[0] - BORDER_SIZE
        ) // SQUARE_SIZE

    def do_move(self, coords_from: tuple[int, int], coords_to: tuple[int, int]) -> None:
        # Do the move on Board and update self.move_done for game Object to notice
        pass

    @staticmethod
    def center_text(
        # helper function to center text on screen
        msg: str,
        pos_x: float,
        pos_y: float,
        color: pygame.Color,
        font: pygame.font,
    ) -> tuple[pygame.Surface, pygame.Rect]:
        text = font.render(msg, True, color)
        text_rect = text.get_rect(center=(pos_x, pos_y))
        return text, text_rect

    @staticmethod
    def sign(x: int) -> int:
        return (x > 0) - (x < 0)
