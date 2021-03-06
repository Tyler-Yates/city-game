import logging
from dataclasses import dataclass
from typing import List, TYPE_CHECKING, Optional

import pygame
from pygame import Surface, Color
from pygame.event import Event

from citygame.src.interfaces.panel import Panel
from citygame.src.state.game_state import GameState
from citygame.src.state.hero_actor import Hero
from citygame.src.state.location_actor import Location
from citygame.src.util.fonts import BASIC_FONT, render_lines_upper_left, render_lines_upper_right, get_rect_for_lines

if TYPE_CHECKING:
    from citygame.src.controllers.scene_controller import SceneController

BACKGROUND_COLOR = "black"

HERO_TEXT_BORDER = 5
HERO_TEXT_SPACING = 5
HERO_TEXT_SIZE = 14
HERO_TEXT_FONT = BASIC_FONT


class HeroPanel(Panel):
    """
    Panel to handle general information in the game.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController", panel_width: int, panel_height: int):
        super().__init__(game_state, scene_controller, panel_width, panel_height)
        self.log = logging.getLogger(self.__class__.__name__)
        self.mouse_x = None
        self.mouse_y = None
        self.hover_hero_rect: Optional[HeroRect] = None

        self.hero_rect_height = get_rect_for_lines(
            border=HERO_TEXT_BORDER,
            spacing=HERO_TEXT_SPACING,
            lines=self._get_hero_information_left(Hero(Location(0, 0, 0, None), self.game_state)),
            size=HERO_TEXT_SIZE,
            font=HERO_TEXT_FONT,
        ).height

        self.hero_rects: List[HeroRect] = []
        self._set_hero_rects()

    def process_input(self, events: List[Event], mouse_x: int, mouse_y: int):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

        self.hover_hero_rect = None
        self.game_state.hover_hero = None
        for hero_rect in self.hero_rects:
            if hero_rect.rect.collidepoint(mouse_x, mouse_y):
                hero_rect.hover = True
                self.game_state.world.hover_location = hero_rect.hero.current_location
                self.hover_hero_rect = hero_rect
                self.game_state.hover_hero = self.hover_hero_rect.hero

        for event in events:
            # Left mouse button released
            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                if self.hover_hero_rect:
                    if self.game_state.selected_hero == self.hover_hero_rect.hero:
                        # Toggle selection state if we are clicking on the selected hero
                        self.game_state.selected_hero = None
                    else:
                        self.game_state.selected_hero = self.hover_hero_rect.hero

    def update(self, time_delta: float):
        pass

    def render(self, surface: Surface):
        surface.fill(BACKGROUND_COLOR)

        BASIC_FONT.render_to(surface, [20, 20], "Heroes", "white", size=22)

        for hero_rect in self.hero_rects:
            if self.game_state.selected_hero == hero_rect.hero:
                hero_rect_color = Color("red")
            elif hero_rect.hover:
                hero_rect_color = Color("white")
            else:
                hero_rect_color = Color(75, 75, 75)
            pygame.draw.rect(surface, hero_rect_color, hero_rect.rect, 1)

            hero = hero_rect.hero

            # Left side
            lines = self._get_hero_information_left(hero)
            render_lines_upper_left(
                surface,
                x=hero_rect.rect.topleft[0],
                y=hero_rect.rect.topleft[1],
                border=HERO_TEXT_BORDER,
                spacing=HERO_TEXT_SPACING,
                lines=lines,
                size=HERO_TEXT_SIZE,
                color=Color("white"),
                font=HERO_TEXT_FONT,
            )

            # Right side
            lines = self._get_hero_information_right(hero)
            render_lines_upper_right(
                surface,
                x=hero_rect.rect.topright[0],
                y=hero_rect.rect.topright[1],
                border=HERO_TEXT_BORDER,
                spacing=HERO_TEXT_SPACING,
                lines=lines,
                size=HERO_TEXT_SIZE,
                color=Color("white"),
                font=HERO_TEXT_FONT,
            )

    @staticmethod
    def _get_hero_information_left(hero: Hero) -> List[str]:
        return [
            f"{hero.name}",
            f"HP: {hero.hp}/{hero.max_hp}",
            f"Location: {hero.current_location.name}",
            f"Destination: {hero.get_destination()}",
        ]

    @staticmethod
    def _get_hero_information_right(hero: Hero) -> List[str]:
        return [f"Level {hero.level}"]

    def _set_hero_rects(self):
        hero_list_start_x = 10
        hero_list_start_y = 50
        width = self.panel_width - hero_list_start_x * 2

        self.hero_rectangles = []
        for i in range(len(self.game_state.heroes)):
            hero = self.game_state.heroes[i]

            y = hero_list_start_y + i * (self.hero_rect_height + 5)
            rect = pygame.Rect(hero_list_start_x, y, width, self.hero_rect_height)

            hero_rect = HeroRect(rect, hero)
            self.hero_rects.append(hero_rect)


@dataclass
class HeroRect:
    rect: pygame.Rect
    hero: Hero
    hover: bool = False
