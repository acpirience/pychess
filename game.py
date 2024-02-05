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
        if self.is_checkmate_stalemate():
            return
        if self.is_treefold_repetition():
            return
        if self.is_fifty_move_rule():
            return
        _ = self.is_dead_position()

    def is_checkmate_stalemate(self) -> bool:
        # Detect checkmate and stalemate
        if not self.board.move_map:
            if self.move_list[len(self.move_list) - 1].endswith("+"):
                self.move_list[len(self.move_list) - 1] += "+"
                self.game_status = "Checkmate !"
            else:
                self.game_status = "Stalemate"

            self.board.board_is_active = False
            self.FEN_list.append(self.board.get_FEN_from_board())
            return True

        return False

    def is_treefold_repetition(self) -> bool:
        # Detect draws : https://www.chess.com/terms/draw-chess
        # Detect Threefold Repetition
        fen_string = self.board.get_FEN_from_board()
        cnt = 0
        for board_fen in reversed(self.FEN_list):
            if board_fen == fen_string:
                cnt += 1
            if cnt >= 2:
                self.game_status = "Draw by Threefold Repetition"
                self.board.board_is_active = False
                self.FEN_list.append(fen_string)
                return True

        return False

    def is_fifty_move_rule(self) -> bool:
        # Detect 50-Move Rule
        if len(self.move_list) < 50:
            # at least 50 move
            return False
        for move in self.move_list[-50:]:
            # no captures
            if "x" in move:
                return False
            # no move by pawn
            if move[0].islower():
                return False

        self.game_status = "Draw by 50-Move Rule"
        self.board.board_is_active = False
        self.FEN_list.append(self.board.get_FEN_from_board())
        return True

    def is_dead_position(self) -> bool:
        # Dead Positions
        # King vs. king
        # King and bishop vs. king
        # King and knight vs. king
        # King and bishop vs. king and bishop of the same color as the opponent's bishop
        piece_list: list[tuple[Piece, int, int]] = []
        for line in range(8):
            for col in range(8):
                if self.board.board_content[line][col]:
                    piece_list.append((self.board.board_content[line][col], line, col))

        if len(piece_list) > 4:
            return False

        if len(piece_list) == 2:  # King vs. king
            self.game_status = "Draw by Dead Position"
            self.board.board_is_active = False
            self.FEN_list.append(self.board.get_FEN_from_board())
            return True

        if len(piece_list) == 3:  # King and bishop vs. king / King and knight vs. king
            # we use this name to avoid a stupid mypy warning if the pieces variable if defined twice ...
            pieces_piece = [x[0].piece for x in piece_list if x[0].piece != "K"]
            if pieces_piece[0] in ["B", "N"]:
                self.game_status = "Draw by Dead Position"
                self.board.board_is_active = False
                self.FEN_list.append(self.board.get_FEN_from_board())
                return True

        if (
            len(piece_list) == 4
        ):  # King and bishop vs. king and bishop of the same color as the opponent's bishop
            pieces = [x for x in piece_list if x[0].piece != "K"]
            if pieces[0][0].piece != "B" or pieces[1][0].piece != "B":  # 2 bishops
                return False
            if pieces[0][0].color == pieces[1][0].color:  # 2 bishops of opposite color
                return False
            if (pieces[0][1] + pieces[0][2]) % 2 == (
                pieces[1][1] + pieces[1][2]
            ) % 2:  # same color as the opponent's bishop
                self.game_status = "Draw by Dead Position"
                self.board.board_is_active = False
                self.FEN_list.append(self.board.get_FEN_from_board())
                return True

        return False

    def _load_assets(self) -> None:
        # load assets used by the object

        # fonts
        # https://www.dafont.com/fr/coolvetica.font
        self.font_turn = pygame.font.Font(os.path.join(FONT_DIR, "coolvetica rg.otf"), 24)

        # https://www.dafont.com/fr/nk57-monospace.font
        self.font_move = pygame.font.Font(os.path.join(FONT_DIR, "nk57-monospace-no-bd.otf"), 14)

    def update(self) -> None:
        self.board.update()
        if self.board.move_done:
            # move done => update board and game objects

            # register FEN Board
            self.FEN_list.append(self.board.get_FEN_from_board())

            # Update flags
            if self.board.move_played.chess_move.startswith("K"):
                self.flags[f"{self.flags['color']}King can castle"] = False

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
        for cnt, move in enumerate(self.move_list):
            if cnt % 2 == 0:
                move = f"{(cnt+2)//2:0>2} {move} "
            else:
                move = f"          - {move}"
            game_canvas.blit(
                self.font_move.render(
                    move,
                    True,
                    pygame.Color("White"),
                ),
                (BOARD_SIZE + BORDER_SIZE, (cnt // 2) * BORDER_SIZE + BORDER_SIZE * 2),
            )
