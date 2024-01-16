"""
        Chess Game
"""
import sys
import pygame


class Game:
    def __init__(self) -> None:
        self.running = True
        self.exit_requested = False
        self.init_window()
        self.init_screen()

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
        self.game_w = 800
        self.game_h = 800
        self.ratio = self.game_w / self.game_h

        self.screen_width = 800
        self.screen_height = 800

        self.blit_origin = (0, 0)
        self.blit_w = self.screen_width
        self.blit_h = self.screen_height

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

    def update(self) -> None:
        pass

    def render(self) -> None:
        self.game_canvas.fill(pygame.Color("Dark Green"))
        self.screen.blit(
            pygame.transform.scale(self.game_canvas, (self.blit_w, self.blit_h)),
            self.blit_origin,
        )
        pygame.display.flip()
        # self.clock.tick(60)


if __name__ == "__main__":
    g = Game()
    while not g.exit_requested:
        g.game_loop()

        pygame.quit()
        sys.exit()
