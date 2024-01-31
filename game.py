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
            self.FEN_list.append(self.board.get_FEN_from_board())

            # Update flags
            if self.board.move_played.chess_move.startswith("K"):
                self.flags[f"{self.flags['color']}King can castle"] = False

            # Check for Null
            # TBD

            # Update Board
            self.board.do_move(self.board.move_played)

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
        self._render_moves(game_canvas)

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

    def _render_moves(self, game_canvas: pygame.Surface) -> None:
        # render turn number and who's turn is it on screen
        moves = ""
        for move in self.move_list:
            moves += f"{move} "
        game_canvas.blit(
            self.font_turn.render(
                moves,
                True,
                pygame.Color("White"),
            ),
            (BORDER_SIZE, BOARD_SIZE),
        )
