"""

Menu used to select type of game: PVP, PVAI, AIVAI

"""

import os

import pygame
from loguru import logger

from common import center_text
from config import FONT_DIR, SCREEN_WIDTH


class StartMenu:
    def __init__(self) -> None:
        self.mouse_coords: tuple[int, int] = (0, 0)
        self.mouse_clicked: dict[str, bool]
        self.menu_done = False
        self.game_type: str
        self._load_assets()
        logger.info("Choosing game type")

    def _load_assets(self) -> None:
        # load assets used by the object TBD make an asset object shared by all

        # fonts
        # https://www.dafont.com/fr/coolvetica.font
        self.font_menu = pygame.font.Font(os.path.join(FONT_DIR, "coolvetica rg.otf"), 36)
        self.font_menu_title = pygame.font.Font(os.path.join(FONT_DIR, "coolvetica rg.otf"), 40)

    def update(self) -> None:
        pass

    def render(self, game_canvas: pygame.Surface) -> None:
        self._render_title(game_canvas)
        self._render_menu(game_canvas)

    def _render_title(self, game_canvas: pygame.Surface) -> None:
        text, text_rect = center_text(
            "CHESS GAME",
            self.font_menu_title,
            pygame.Color("White"),
            (SCREEN_WIDTH / 2, 40),
        )
        game_canvas.blit(text, text_rect)

    def _render_menu(self, game_canvas: pygame.Surface) -> None:
        text, text_rect = center_text(
            "Please choose Game type",
            self.font_menu,
            pygame.Color("White"),
            (SCREEN_WIDTH / 2, 150),
        )
        game_canvas.blit(text, text_rect)

        for line, menu_item in enumerate(
            ["Player versus Player", "Player as White vers AI", "Player as Black vers AI"]
        ):
            text, text_rect = center_text(
                menu_item,
                self.font_menu,
                pygame.Color("White"),
                (SCREEN_WIDTH / 2, 300 + line * 100),
            )

            color = pygame.Color("Dark Green")

            pos_x = text_rect.x - 10
            pos_y = text_rect.y - 5
            width = text_rect.width + 20
            height = text_rect.height + 10

            if (pos_x < self.mouse_coords[0] < pos_x + width) and (
                pos_y < self.mouse_coords[1] < pos_y + height
            ):
                color = pygame.Color("Dark Gray")
                if self.mouse_clicked["BUTTONDOWN"]:
                    logger.info(menu_item)
                    if line == 0:
                        self.game_type = "PVP"
                        self.menu_done = True

            pygame.draw.rect(
                game_canvas,
                color,
                pygame.Rect(
                    pos_x,
                    pos_y,
                    width,
                    height,
                ),
                0,
                5,
            )

            game_canvas.blit(text, text_rect)
