import logging
import math
from typing import List, TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.event import Event

from citygame.src.constants.game_constants import GAME_WIDTH_PX, GAME_HEIGHT_PX
from citygame.src.constants.location_state_enum import LocationState
from citygame.src.constants.world_constants import LOCATION_DOT_RADIUS
from citygame.src.frameprocessors.information_panel import GeneralInformationPanel
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
        self.map_offset_x = abs(self.map_viewport_surface.get_width() - self.map_surface.get_width()) // 2
        self.map_offset_y = abs(self.map_viewport_surface.get_height() - self.map_surface.get_height()) // 2

        self.map_viewport_offset_x = abs(GAME_WIDTH_PX - self.map_viewport_surface.get_width()) // 2
        self.map_viewport_offset_y = abs(GAME_HEIGHT_PX - self.map_viewport_surface.get_height()) // 2

        # Panels
        panel_width = (GAME_WIDTH_PX - MAP_VIEWPORT_SIZE) // 2
        panel_height = GAME_HEIGHT_PX

        self.left_panel_surface = Surface((panel_width, panel_height))
        self.right_panel_surface = Surface((panel_width, panel_height))

        self.general_information_panel = GeneralInformationPanel(game_state, scene_controller, panel_width, panel_height)

    def process_input(self, events: List[Event]):
        mouse_pos = pygame.mouse.get_pos()
        # Mouse seems to be off by a little bit so offset it
        mouse_x_abs = mouse_pos[0] - 1
        mouse_y_abs = mouse_pos[1] - 1

        # Take into account the position within the window when processing mouse position on the map
        mouse_x_map = mouse_x_abs - self.map_offset_x - self.map_viewport_offset_x
        mouse_y_map = mouse_y_abs - self.map_offset_y - self.map_viewport_offset_y

        # See if any locations are the new hover location and deal with mouse actions on that location
        self.game_state.world.hover_location = None
        for location in self.game_state.world.locations:
            # Reset the hover status for every location
            location.hover = False

            # For discovered locations, detect if this location is the new hover location
            if location.location_state != LocationState.HIDDEN:
                distance = math.sqrt(math.pow(location.x - mouse_x_map, 2) + math.pow(location.y - mouse_y_map, 2))
                if distance <= (LOCATION_DOT_RADIUS + 0.1):
                    self.game_state.world.hover_location = location

        # Process all the events
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.game_state.world.hover_location:
                    self.game_state.world.location_conquered(self.game_state.world.hover_location)

        # Set the hover status now that we have redrawn everything
        if self.game_state.world.hover_location:
            self.game_state.world.hover_location.hover = True

        # Panels
        self.general_information_panel.process_input(events, mouse_x_abs, mouse_y_abs)

    def update(self, time_delta: float):
        # Panels
        self.general_information_panel.update(time_delta)

    def render(self, screen: Surface):
        screen.fill(BACKGROUND_COLOR)

        # Render the world to the map surface
        self.game_state.world.render(self.map_surface)
        # Render the hover location to change the dot ring color
        if self.game_state.world.hover_location:
            self.game_state.world.hover_location.render(self.map_surface)

        # Render the map surface to the map viewport, centered
        self.map_viewport_surface.blit(self.map_surface, (self.map_offset_x, self.map_offset_y))

        # Render the map viewport
        screen.blit(self.map_viewport_surface, (self.map_viewport_offset_x, self.map_viewport_offset_y))

        # Panels
        self.general_information_panel.render(self.left_panel_surface)
        screen.blit(self.left_panel_surface, (0, 0))
