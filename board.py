"""

class responsible to draw the chess board in its current state

"""

import pygame

COLOR_SCHEME_LIST = {
    "BLACK": ["#D6D7D4", "#211E24"],
    "WOOD": ["#F0D1A1", "#9F4A25"],
    "GREEN": ["#F0D1A1", "#537C49"],
}

SQUARE_SIZE = 100


class Board:
    def __init__(
        self,
        orientation: str = "STANDARD",
        color_scheme: str = "BLACK",
    ) -> None:
        self.orientation = orientation
        self.color_scheme = color_scheme
        print(self.color_scheme)

    def render(self, game_canvas: pygame.Surface) -> None:
        self._render_board(game_canvas)

    def _render_board(self, game_canvas: pygame.Surface) -> None:
        colors = COLOR_SCHEME_LIST[self.color_scheme]
        for x in range(8):
            for y in range(8):
                square = pygame.Rect(
                    ((x % 8) * SQUARE_SIZE, (y % 8) * SQUARE_SIZE),
                    (SQUARE_SIZE, SQUARE_SIZE),
                )

                pygame.draw.rect(game_canvas, colors[(x + y) % 2], square)
