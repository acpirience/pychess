"""

Chess game

"""

from board import Board, BORDER_SIZE, SQUARE_SIZE
import pygame
import os
from loguru import logger
from config import FONT_DIR


FEN_INITIAL_BOARD = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
BOARD_SIZE = (SQUARE_SIZE * 8) + (BORDER_SIZE * 2)


class Game:
    def __init__(self) -> None:
        self.move_list: list[list[str]] = [[]]
        self.FEN_list: list[str] = []
        self.white_plays = True
        self.turn = 1

        # Board
        self.board = Board(True, "WOOD")
        self.board.load_board_from_FEN(FEN_INITIAL_BOARD)

        # assets
        self._load_assets()

    def _load_assets(self) -> None:
        # fonts
        # https://www.dafont.com/fr/coolvetica.font
        self.font_turn = pygame.font.Font(
            os.path.join(FONT_DIR, "coolvetica rg.otf"), 24
        )
        logger.info("Loading font_turn: 'coolvetica rg.otf' 24")

    def update(self) -> None:
        pass

    def render(self, game_canvas: pygame.Surface) -> None:
        self.board.render(game_canvas)
        self._render_turn(game_canvas)

    def _render_turn(self, game_canvas: pygame.Surface) -> None:
        game_canvas.blit(
            self.font_turn.render(
                f"TURN {self.turn}, {'White' if self.white_plays else 'Black'} plays",
                True,
                pygame.Color("White"),
            ),
            (BOARD_SIZE + BORDER_SIZE, BORDER_SIZE / 2),
        )
