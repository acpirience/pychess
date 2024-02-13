"""
        Chess Game: point of entry for batched games to compare engines
"""

from loguru import logger

from game import COLOR_TO_TEXT, Game


class BatchChess:
    def __init__(self, nb_game: int = 1) -> None:
        self.exit_requested = False

        self.game_status = "started"
        self.game: Game
        self.nb_game_left = nb_game
        self.results: dict[str, int] = {
            "Black wins": 0,
            "White wins": 0,
            "Null: Stalemate": 0,
            "Null: Draw by Threefold Repetition": 0,
            "Null: Draw by 50-Move Rule": 0,
            "Null: Draw by Dead Position": 0,
        }

    def game_loop(self) -> None:
        while not self.exit_requested:
            self.update()

    def update(self) -> None:
        if self.game_status == "started":
            logger.info(f"{self.nb_game_left} games left")
            self.game = Game("AIVAI", "", True)
            self.game_status = "game started"

        if self.game_status == "game started":
            if self.game.game_status == "Started":
                self.game.update()
            else:
                self.update_results()
                self.nb_game_left -= 1
                if self.nb_game_left > 0:
                    self.game_status = "started"
                else:
                    self.exit_requested = True

    def update_results(self) -> None:
        if self.game.game_status != "Checkmate !":
            status = f"Null: {self.game.game_status}"
        else:
            winner = "w"
            if self.game.flags["color"] == "w":
                winner = "b"
            status = f"{COLOR_TO_TEXT[winner]} wins"

        logger.warning(status)
        self.results[status] += 1


if __name__ == "__main__":
    g = BatchChess(200)
    g.game_loop()
    logger.info("*" * 40)
    for result in g.results:
        logger.info(f"{result : <36}: {g.results[result]}")
