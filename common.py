"""

Helper functions

"""

import pygame


def center_text(
    text: str, font: pygame.font, color: pygame.color, text_center: tuple[float, float]
) -> tuple[pygame.surface, pygame.Rect]:
    ret_text = font.render(
        text,
        True,
        color,
    )

    text_rect = ret_text.get_rect(center=text_center)

    return ret_text, text_rect
