import logging
from typing import List, TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.event import Event

from citygame.src.constants.game_constants import GAME_WIDTH_PX, GAME_HEIGHT_PX
from citygame.src.frameprocessors.general_information_panel import GeneralInformationPanel
from citygame.src.frameprocessors.hero_panel import HeroPanel
from citygame.src.frameprocessors.map_panel import MapPanel
from citygame.src.interfaces.scene import Scene
from citygame.src.state.game_state import GameState
from citygame.src.util.map_tile import MapTile

if TYPE_CHECKING:
    from citygame.src.controllers.scene_controller import SceneController


BACKGROUND_COLOR = "black"

MAP_PANEL_SIZE = 720


class GameScene(Scene):
    """
    Scene that handles actual gameplay.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController"):
        super().__init__(game_state, scene_controller)
        self.log = logging.getLogger(self.__class__.__name__)

        # Map panel
        self.map_panel_surface = Surface((MAP_PANEL_SIZE, MAP_PANEL_SIZE))
        self.map_panel_surface.fill(MapTile.get_rgb_value(MapTile.DEEP_WATER.value))
        self.map_panel_offset_x = abs(GAME_WIDTH_PX - self.map_panel_surface.get_width()) // 2
        self.map_panel_offset_y = abs(GAME_HEIGHT_PX - self.map_panel_surface.get_height()) // 2
        self.map_panel = MapPanel(game_state, scene_controller, MAP_PANEL_SIZE, MAP_PANEL_SIZE)

        # Left Panel
        panel_width = (GAME_WIDTH_PX - MAP_PANEL_SIZE) // 2
        panel_height = GAME_HEIGHT_PX
        self.left_panel_surface = Surface((panel_width, panel_height))
        self.general_information_panel = GeneralInformationPanel(
            game_state, scene_controller, panel_width, panel_height
        )
        self.left_panel = self.general_information_panel

        # Right panel
        self.right_panel_surface = Surface((panel_width, panel_height))
        self.hero_panel = HeroPanel(game_state, scene_controller, panel_width, panel_height)
        self.right_panel = self.hero_panel
        self.right_panel_offset_x = abs(GAME_WIDTH_PX - self.right_panel_surface.get_width())
        self.right_panel_offset_y = 0

    def process_input(self, events: List[Event]):
        mouse_pos = pygame.mouse.get_pos()
        # Mouse seems to be off by a little bit so offset it
        mouse_x_abs = mouse_pos[0] - 1
        mouse_y_abs = mouse_pos[1] - 1

        # Reset hover state
        for location in self.game_state.world.locations:
            location.hover = False
        for hero_rect in self.hero_panel.hero_rects:
            hero_rect.hover = False

        # Map panel
        self.map_panel.process_input(
            events, mouse_x_abs - self.map_panel_offset_x, mouse_y_abs - self.map_panel_offset_y
        )

        # Left panel is drawn at (0, 0) so no need to adjust the mouse position
        self.left_panel.process_input(events, mouse_x_abs, mouse_y_abs)

        # Right panel
        self.right_panel.process_input(
            events, mouse_x_abs - self.right_panel_offset_x, mouse_y_abs - self.right_panel_offset_y
        )

    def update(self, time_delta: float):
        # Panels
        self.map_panel.update(time_delta)
        self.left_panel.update(time_delta)
        self.right_panel.update(time_delta)

    def render(self, screen: Surface):
        screen.fill(BACKGROUND_COLOR)

        # Map panel
        self.map_panel.render(self.map_panel_surface)
        screen.blit(self.map_panel_surface, (self.map_panel_offset_x, self.map_panel_offset_y))

        # Left panel
        self.left_panel.render(self.left_panel_surface)
        screen.blit(self.left_panel_surface, (0, 0))

        # Right panel
        self.right_panel.render(self.right_panel_surface)
        screen.blit(self.right_panel_surface, (self.right_panel_offset_x, self.right_panel_offset_y))
