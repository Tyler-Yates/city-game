import logging
from typing import List, TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.event import Event

from citygame.src.constants.game_constants import GAME_WIDTH_PX, GAME_HEIGHT_PX
from citygame.src.frameprocessors.general_information_panel import GeneralInformationPanel
from citygame.src.frameprocessors.map_panel import MapPanel
from citygame.src.interfaces.scene import Scene
from citygame.src.state.game_state import GameState
from citygame.src.util.map_tile import MapTile

if TYPE_CHECKING:
    from citygame.src.controllers.scene_controller import SceneController


BACKGROUND_COLOR = "black"

map_panel_SIZE = 720


class GameScene(Scene):
    """
    Scene that handles actual gameplay.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController"):
        super().__init__(game_state, scene_controller)
        self.log = logging.getLogger(self.__class__.__name__)

        # Map panel
        self.map_panel_surface = Surface((map_panel_SIZE, map_panel_SIZE))
        self.map_panel_surface.fill(MapTile.get_rgb_value(MapTile.DEEP_WATER.value))
        self.map_panel_offset_x = abs(GAME_WIDTH_PX - self.map_panel_surface.get_width()) // 2
        self.map_panel_offset_y = abs(GAME_HEIGHT_PX - self.map_panel_surface.get_height()) // 2

        self.map_panel = MapPanel(game_state, scene_controller, map_panel_SIZE, map_panel_SIZE)

        # Side Panels
        panel_width = (GAME_WIDTH_PX - map_panel_SIZE) // 2
        panel_height = GAME_HEIGHT_PX
        self.left_panel_surface = Surface((panel_width, panel_height))
        self.right_panel_surface = Surface((panel_width, panel_height))

        self.left_panel = GeneralInformationPanel(game_state, scene_controller, panel_width, panel_height)

    def process_input(self, events: List[Event]):
        mouse_pos = pygame.mouse.get_pos()
        # Mouse seems to be off by a little bit so offset it
        mouse_x_abs = mouse_pos[0] - 1
        mouse_y_abs = mouse_pos[1] - 1

        # Map panel
        self.map_panel.process_input(
            events, mouse_x_abs - self.map_panel_offset_x, mouse_y_abs - self.map_panel_offset_y
        )

        # Side panels
        self.left_panel.process_input(events, mouse_x_abs, mouse_y_abs)

    def update(self, time_delta: float):
        # Panels
        self.map_panel.update(time_delta)
        self.left_panel.update(time_delta)

    def render(self, screen: Surface):
        screen.fill(BACKGROUND_COLOR)

        # Render the map panel
        self.map_panel.render(self.map_panel_surface)
        screen.blit(self.map_panel_surface, (self.map_panel_offset_x, self.map_panel_offset_y))

        # Panels
        self.left_panel.render(self.left_panel_surface)
        screen.blit(self.left_panel_surface, (0, 0))
