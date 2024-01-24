"""

Chess game

"""

import os

import pygame
from loguru import logger

from board import BORDER_SIZE, SQUARE_SIZE, Board
from config import FONT_DIR
from position import Position

FEN_INITIAL_BOARD = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
# FEN_INITIAL_BOARD = "rp4pr/pppppppp/8/8/8/8/PPPPPPPP/RP4PR"
BOARD_SIZE = (SQUARE_SIZE * 8) + (BORDER_SIZE * 2)


class Game:
    def __init__(self) -> None:
        self.move_list: list[list[str]] = [[]]
        self.FEN_list: list[str] = []
        # dict containing information on the game such as
        # who is to play / is a king in check / have king moved (for castle)
        self.flags: dict[str, str] = {"color": "w", "in_check": "", "previous_move": ""}
        self.turn = 1

        # Board
        self.board = Board(True, "WOOD")
        self.board.load_board_from_FEN(FEN_INITIAL_BOARD)

        # assets
        self._load_assets()

        # start
        self.position = Position(self.board.board_content, self.flags)
        self.possible_moves = self.position.get_possible_moves()

    def _load_assets(self) -> None:
        # load assets used by the object

        # fonts
        # https://www.dafont.com/fr/coolvetica.font
        self.font_turn = pygame.font.Font(os.path.join(FONT_DIR, "coolvetica rg.otf"), 24)
        logger.info("Loading font_turn: 'coolvetica rg.otf' 24")

    def update(self) -> None:
        pass

    def render(self, game_canvas: pygame.Surface) -> None:
        # render Board and game informations on screen
        self.board.render(game_canvas)
        self._render_turn(game_canvas)

    def _render_turn(self, game_canvas: pygame.Surface) -> None:
        # render turn number and who's turn is it on screen
        game_canvas.blit(
            self.font_turn.render(
                f"TURN {self.turn}, {'White' if self.flags['color'] == 'w' else 'Black'} plays",
                True,
                pygame.Color("White"),
            ),
            (BOARD_SIZE + BORDER_SIZE, BORDER_SIZE / 2),
        )
