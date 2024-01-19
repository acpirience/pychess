"""

class responsible to draw the chess board in its current state

"""

import glob
import os

import pygame
from loguru import logger

from config import FONT_DIR, IMG_DIR

COLOR_SCHEME_LIST = {
    "BLACK": ["#D6D7D4", "#211E24", "#000000"],
    "WOOD": ["#F0D1A1", "#9F4A25", "#861C00"],
    "GREEN": ["#F0D1A1", "#537C49", "#234C19"],
}

SQUARE_SIZE = 100
BORDER_SIZE = 25


class Board:
    def __init__(
        self,
        white_is_south: bool = True,
        color_scheme: str = "BLACK",
    ) -> None:
        self.white_is_south = white_is_south
        self.color_scheme = color_scheme
        self.board_content: list[list[str]] = [[] for _ in range(8)]
        self._load_assets()

    def _load_assets(self) -> None:
        # fonts
        # https://www.dafont.com/fr/coolvetica.font
        self.font_board_marks = pygame.font.Font(os.path.join(FONT_DIR, "coolvetica rg.otf"), 16)
        logger.info("Loading font_board_marks: 'coolvetica rg.otf' 16")

        # Images : chess pieces
        # https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces
        self.piece_list = {}
        png_list = [
            x.removeprefix(IMG_DIR + os.sep).removesuffix(".png")
            for x in glob.glob(os.path.join(IMG_DIR, "*.png"))
        ]
        for piece in png_list:
            self.piece_list[piece] = pygame.image.load(os.path.join(IMG_DIR, f"{piece}.png"))
            logger.info(f"Loading image {piece}: {piece}.png")

    def render(self, game_canvas: pygame.Surface) -> None:
        self.square_colors = COLOR_SCHEME_LIST[self.color_scheme]
        self._render_back(game_canvas)
        self._render_board(game_canvas)
        self._render_marks(game_canvas)
        self._render_pieces(game_canvas)

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
        back_length = (BORDER_SIZE * 2) + (SQUARE_SIZE * 8)
        back = pygame.Rect((0, 0), (back_length, back_length))
        pygame.draw.rect(game_canvas, self.square_colors[2], back)

    def _render_marks(self, game_canvas: pygame.Surface) -> None:
        numbers = [str(x + 1) for x in reversed(range(8))]
        letters = [chr(x + 65) for x in range(8)]
        if not self.white_is_south:
            numbers.reverse()
            letters.reverse()

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

    def _render_pieces(self, game_canvas: pygame.Surface) -> None:
        if self.white_is_south:
            board = self.board_content
        else:
            board = [self.board_content[x][::-1] for x in reversed(range(8))]

        cur_line = 0
        for line in board:
            cur_col = 0
            while cur_col < 8:
                if line[cur_col]:
                    game_canvas.blit(
                        self.piece_list[line[cur_col]],
                        (
                            BORDER_SIZE + (SQUARE_SIZE * cur_col),
                            BORDER_SIZE + (SQUARE_SIZE * cur_line),
                        ),
                    )
                cur_col += 1
            cur_line += 1

    def load_board_from_FEN(self, fen_string: str) -> None:
        # https://www.chess.com/terms/fen-chess
        cur_board_line = 0
        self.board_content = [[] for _ in range(8)]
        for line in fen_string.split("/"):
            for x in line:
                if x.isdigit():
                    for _ in range(int(x)):
                        self.board_content[cur_board_line].append("")
                else:
                    self.board_content[cur_board_line].append(
                        x.upper() + ("b" if x.islower() else "w")
                    )
            cur_board_line += 1

    @staticmethod
    def center_text(
        msg: str, pos_x: float, pos_y: float, color: pygame.Color, font: pygame.font
    ) -> tuple[pygame.Surface, pygame.Rect]:
        text = font.render(msg, True, color)
        text_rect = text.get_rect(center=(pos_x, pos_y))
        return text, text_rect
