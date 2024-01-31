"""

Chess game

"""

import os

import pygame
from loguru import logger

from board import BORDER_SIZE, SQUARE_SIZE, Board
from config import FONT_DIR
from piece import Piece
from position import Position

FEN_INITIAL_BOARD = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
FEN_INITIAL_BOARD = "rnbqkbnr/pppppppp/8/8/8/1P6/8/RNBQK2R"

BOARD_SIZE = (SQUARE_SIZE * 8) + (BORDER_SIZE * 2)


class Game:
    def __init__(self) -> None:
        logger.info("Starting Game")
        self.move_list: list[str] = []
        self.FEN_list: list[str] = []
        # dict containing information on the game such as
        # who is to play / is a king in check / have king moved (for castle)
        self.flags: dict[str, str | bool] = {
            "color": "w",
            "in_check": "",
            "wKing can castle": True,
            "bKing can castle": True,
            "previous_move": "",
        }
        self.turn = 1

        # Board
        self.board = Board("WOOD")
        self.board.load_board_from_FEN(FEN_INITIAL_BOARD)

        # assets
        self._load_assets()

        # start
        self.next_turn()

    def next_turn(self) -> None:
        self.board.new_turn()
        self.position = Position(self.board.board_content, self.flags)
        self.board.move_map = self.position.move_map
        # check for checkmate
        # TBD

    def _load_assets(self) -> None:
        # load assets used by the object

        # fonts
        # https://www.dafont.com/fr/coolvetica.font
        self.font_turn = pygame.font.Font(os.path.join(FONT_DIR, "coolvetica rg.otf"), 24)

    def update(self) -> None:
        self.board.update()
        if self.board.move_done:
            # move done => update board and gamre objects
            # register move
            self.flags["previous_move"] = self.board.move_played.chess_move
            self.move_list.append(self.board.move_played.chess_move)

            # register FEN Board
            # TBD

            # register FEN Board
            # TBD

            # Update all flags
            # TBD

            # Check for Null
            # TBD

            # Update Board
            self.board.board_content[self.board.move_played.square_to[0]][
                self.board.move_played.square_to[1]
            ] = self.board.board_content[self.board.move_played.square_from[0]][
                self.board.move_played.square_from[1]
            ]
            self.board.board_content[self.board.move_played.square_from[0]][
                self.board.move_played.square_from[1]
            ] = Piece()

            # switch Player
            if self.flags["color"] == "w":
                self.flags["color"] = "b"
            else:
                self.flags["color"] = "w"
                self.turn += 1

            self.next_turn()

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
