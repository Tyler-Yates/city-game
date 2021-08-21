from typing import Tuple

import pygame.freetype
from pygame.surface import Surface

pygame.freetype.init()

BASIC_FONT = pygame.freetype.SysFont("Arial", 24)
MONOSPACE_FONT = pygame.freetype.SysFont("Courier New", 24)


def render_with_outline(
    screen: Surface,
    font,
    draw_position: Tuple[int, int],
    text: str,
    size: int,
    text_color,
    outline_color,
    outline_size_px: int = 1,
):
    """
    Renders the given text with an outline.

    Args:
        screen: the surface to draw to
        font: the font to use
        draw_position: x,y coordinates of where to draw the text
        text: the text to draw
        size: the size of the text
        text_color: the color of the text
        outline_color: the color of the outline
        outline_size_px: the size of the outline in pixels
    """
    pos_x = draw_position[0]
    pos_y = draw_position[1]
    font.render_to(screen, (pos_x - outline_size_px, pos_y - outline_size_px), text, outline_color, size=size)
    font.render_to(screen, (pos_x + outline_size_px, pos_y - outline_size_px), text, outline_color, size=size)
    font.render_to(screen, (pos_x - outline_size_px, pos_y + outline_size_px), text, outline_color, size=size)
    font.render_to(screen, (pos_x + outline_size_px, pos_y + outline_size_px), text, outline_color, size=size)
    font.render_to(screen, draw_position, text, text_color, size=size)
