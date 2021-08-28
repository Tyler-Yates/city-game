import logging
from dataclasses import dataclass
from typing import List, TYPE_CHECKING

import pygame
from pygame import Surface, Color
from pygame.event import Event

from citygame.src.interfaces.panel import Panel
from citygame.src.state.game_state import GameState
from citygame.src.state.hero_actor import Hero
from citygame.src.util.fonts import BASIC_FONT, render_font_upper_left

if TYPE_CHECKING:
    from citygame.src.controllers.scene_controller import SceneController

BACKGROUND_COLOR = "black"

HERO_RECT_HEIGHT = 50


class HeroPanel(Panel):
    """
    Panel to handle general information in the game.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController", panel_width: int, panel_height: int):
        super().__init__(game_state, scene_controller, panel_width, panel_height)
        self.log = logging.getLogger(self.__class__.__name__)
        self.mouse_x = None
        self.mouse_y = None

        self.hero_rects: List[HeroRect] = []
        self._set_hero_rects()

    def process_input(self, events: List[Event], mouse_x: int, mouse_y: int):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

        for hero_rect in self.hero_rects:
            if hero_rect.rect.collidepoint(mouse_x, mouse_y):
                hero_rect.hover = True
            else:
                hero_rect.hover = False

    def update(self, time_delta: float):
        pass

    def render(self, surface: Surface):
        surface.fill(BACKGROUND_COLOR)

        BASIC_FONT.render_to(surface, [20, 20], "Heroes", "white", size=22)

        for hero_rect in self.hero_rects:
            if hero_rect.hover:
                pygame.draw.rect(surface, Color("red"), hero_rect.rect, 1)
            render_font_upper_left(
                surface,
                x=hero_rect.rect.topleft[0],
                y=hero_rect.rect.topleft[1],
                spacing=5,
                text=hero_rect.hero.name,
                size=14,
                color=Color("white"),
            )

    def _set_hero_rects(self):
        hero_list_start_x = 10
        hero_list_start_y = 50
        width = self.panel_width - hero_list_start_x * 2

        self.hero_rectangles = []
        for i in range(len(self.game_state.heroes)):
            hero = self.game_state.heroes[i]

            y = hero_list_start_y + i * HERO_RECT_HEIGHT
            rect = pygame.Rect(hero_list_start_x, y, width, HERO_RECT_HEIGHT)

            hero_rect = HeroRect(rect, hero)
            self.hero_rects.append(hero_rect)


@dataclass
class HeroRect:
    rect: pygame.Rect
    hero: Hero
    hover: bool = False
