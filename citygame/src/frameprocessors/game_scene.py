import logging
import math
from typing import List, TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.event import Event

from citygame.src.constants.world_constants import LOCATION_DOT_RADIUS
from citygame.src.interfaces.scene import Scene
from citygame.src.state.game_state import GameState
from citygame.src.util.map_tile import MapTile

if TYPE_CHECKING:
    from citygame.src.controllers.scene_controller import SceneController


BACKGROUND_COLOR = "black"

MAP_VIEWPORT_SIZE = 720


class GameScene(Scene):
    """
    Scene that handles actual gameplay.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController"):
        super().__init__(game_state, scene_controller)
        self.log = logging.getLogger(self.__class__.__name__)

        self.map_viewport_surface = Surface((MAP_VIEWPORT_SIZE, MAP_VIEWPORT_SIZE))
        self.map_viewport_surface.fill(MapTile.get_rgb_value(MapTile.DEEP_WATER.value))

        self.map_surface = Surface((self.game_state.map_size, self.game_state.map_size))
        self.map_viewport_offset_x = abs(self.map_viewport_surface.get_width() - self.map_surface.get_width()) // 2
        self.map_viewport_offset_y = abs(self.map_viewport_surface.get_height() - self.map_surface.get_height()) // 2

    def process_input(self, events: List[Event]):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x_abs = mouse_pos[0]
        mouse_y_abs = mouse_pos[1]

        mouse_x_map = mouse_x_abs - self.map_viewport_offset_x
        mouse_y_map = mouse_y_abs - self.map_viewport_offset_y

        # See if any locations are the new hover location and deal with mouse actions on that location
        self.game_state.world.hover_location = None
        for location in self.game_state.world.locations:
            distance = math.sqrt(math.pow(location.x - mouse_x_map, 2) + math.pow(location.y - mouse_y_map, 2))
            if distance <= LOCATION_DOT_RADIUS:
                self.game_state.world.hover_location = location
                location.hover = True

                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.game_state.world.location_conquered(location)
            else:
                location.hover = False

    def update(self, time_delta: float):
        pass

    def render(self, screen: Surface):
        screen.fill(BACKGROUND_COLOR)

        # Render the world to the map surface
        self.game_state.world.render(self.map_surface)
        # Render the hover location to change the dot ring color
        if self.game_state.world.hover_location:
            self.game_state.world.hover_location.render(self.map_surface)

        # Render the map surface to the map viewport, centered
        self.map_viewport_surface.blit(self.map_surface, (self.map_viewport_offset_x, self.map_viewport_offset_y))

        # Render the map viewport
        screen.blit(self.map_viewport_surface, (0, 0))
