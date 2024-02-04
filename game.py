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
        self.game_status = "Started"
        self.turn = 1

        # Board
        self.board = Board("WOOD")
        self.board.load_board_from_FEN(FEN_INITIAL_BOARD)

        # assets
        self._load_assets()

        # start
        self.next_move()

    def next_move(self) -> None:
        self.board.new_move()
        self.position = Position(self.board.board_content, self.flags)
        self.board.move_map = self.position.move_map

        # check for end of game
        self.detect_end_of_game()

    def detect_end_of_game(self) -> None:
        # Detect checkmate and stalemate
        if not self.board.move_map:
            if self.move_list[len(self.move_list) - 1].endswith("+"):
                self.move_list[len(self.move_list) - 1] += "+"
                self.game_status = "Checkmate !"
            else:
                self.game_status = "Stalemate"
            self.FEN_list.append(self.board.get_FEN_from_board())

        # Detect Threefold Repetition
        # TBD

        # Detect 50-Move Rule
        # TBD

        # Dead Position
        # TBD

    def _load_assets(self) -> None:
        # load assets used by the object

        # fonts
        # https://www.dafont.com/fr/coolvetica.font
        self.font_turn = pygame.font.Font(os.path.join(FONT_DIR, "coolvetica rg.otf"), 24)

    def update(self) -> None:
        self.board.update()
        if self.board.move_done:
            # move done => update board and game objects

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

            # check if opposite king is in check
            if self.position.king_is_in_check(self.board.board_content):
                logger.info(f"{self.flags['color']} King is in check")
                self.board.move_played.chess_move += "+"

            # register move
            self.flags["previous_move"] = self.board.move_played.chess_move
            self.move_list.append(self.board.move_played.chess_move)

            if self.flags["color"] == "w":
                self.turn += 1

            self.next_move()

    def render(self, game_canvas: pygame.Surface) -> None:
        # render Board and game informations on screen
        self.board.render(game_canvas)
        self._render_turn(game_canvas)
        self._render_moves(game_canvas)

    def _render_turn(self, game_canvas: pygame.Surface) -> None:
        # render turn number and who's turn is it on screen
        render_str = f"TURN {self.turn}, "
        if self.game_status == "Started":
            render_str += f"{'White' if self.flags['color'] == 'w' else 'Black'} plays"
        else:
            render_str += f"{self.game_status}"

        game_canvas.blit(
            self.font_turn.render(
                render_str,
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
