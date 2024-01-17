"""

class responsible to draw the chess board in its current state

"""

import pygame
import os

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
        self._load_assets()

    def _load_assets(self) -> None:
        self.assets_dir = os.path.join("assets")
        self.font_dir = os.path.join(self.assets_dir, "fonts")

        # fonts
        # https://www.dafont.com/fr/coolvetica.font
        self.font_board_marks = pygame.font.Font(
            os.path.join(self.font_dir, "coolvetica rg.otf"), 16
        )

    def render(self, game_canvas: pygame.Surface) -> None:
        self.square_colors = COLOR_SCHEME_LIST[self.color_scheme]
        self._render_back(game_canvas)
        self._render_board(game_canvas)
        self._render_marks(game_canvas)

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

    @staticmethod
    def center_text(
        msg: str, pos_x: float, pos_y: float, color: pygame.Color, font: pygame.font
    ) -> tuple[pygame.Surface, pygame.Rect]:
        text = font.render(msg, True, color)
        text_rect = text.get_rect(center=(pos_x, pos_y))
        return text, text_rect
