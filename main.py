"""
        Chess Game
"""
import sys

import pygame

from config import SCREEN_HEIGHT, SCREEN_WIDTH
from game import Game


class Chess:
    def __init__(self) -> None:
        self.running = True
        self.exit_requested = False

        # screen
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.game_w = self.screen_width
        self.game_h = self.screen_height

        self.init_window()
        self.init_screen()
        self.game = Game()

        # Mouse
        pygame.mouse.set_visible(True)
        self.mouse_coords = (0, 0)
        self.mouse_clicked = {"BUTTONUP": False, "BUTTONDOWN": False}

    def game_loop(self) -> None:
        while self.running:
            self.get_events()
            self.update()
            self.render()
        self.exit_requested = True

    def init_window(self) -> None:
        pygame.init()
        pygame.display.set_caption("PyChess")

    def init_screen(self) -> None:
        # Screen and aspect ratio
        self.game_ratio = self.game_w / self.game_h
        self.blit_w = self.screen_width
        self.blit_h = self.screen_height
        self.blit_origin = (0, 0)

        self.monitor_size = [
            pygame.display.Info().current_w,
            pygame.display.Info().current_h,
        ]

        self.game_canvas = pygame.Surface((self.game_w, self.game_h))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def get_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEMOTION:
                self.mouse_coords = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_clicked["BUTTONDOWN"] = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_clicked["BUTTONDOWN"] = True

    def update(self) -> None:
        self.game.board.mouse_coords = self.mouse_coords
        self.game.board.mouse_clicked = self.mouse_clicked
        self.game.update()

    def render(self) -> None:
        self.game_canvas.fill(pygame.Color("Dark Green"))

        self.game.render(self.game_canvas)

        self.screen.blit(
            pygame.transform.scale(self.game_canvas, (self.blit_w, self.blit_h)),
            self.blit_origin,
        )
        pygame.display.flip()
        # self.clock.tick(60)


if __name__ == "__main__":
    g = Chess()
    while not g.exit_requested:
        g.game_loop()

        pygame.quit()
        sys.exit()
