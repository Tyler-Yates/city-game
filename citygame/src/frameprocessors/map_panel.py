import logging
import math
from typing import List, TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.event import Event

from citygame.src.constants.location_state_enum import LocationState
from citygame.src.constants.world_constants import LOCATION_DOT_RADIUS
from citygame.src.interfaces.panel import Panel
from citygame.src.state.game_state import GameState

if TYPE_CHECKING:
    from citygame.src.controllers.scene_controller import SceneController


BACKGROUND_COLOR = "black"


class MapPanel(Panel):
    """
    Panel to display the map.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController", panel_width: int, panel_height: int):
        super().__init__(game_state, scene_controller, panel_width, panel_height)
        self.log = logging.getLogger(self.__class__.__name__)

        self.map_surface = Surface((self.game_state.map_size, self.game_state.map_size))
        self.map_offset_x = abs(panel_width - self.map_surface.get_width()) // 2
        self.map_offset_y = abs(panel_height - self.map_surface.get_height()) // 2

    def process_input(self, events: List[Event], mouse_x: int, mouse_y: int):
        # Take into account the position within the window when processing mouse position on the map
        mouse_x_map = mouse_x - self.map_offset_x
        mouse_y_map = mouse_y - self.map_offset_y

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

    def update(self, time_delta: float):
        pass

    def render(self, surface: Surface):
        # Render the world to the map surface
        self.game_state.world.render(self.map_surface)
        # Render the hover location to change the dot ring color
        if self.game_state.world.hover_location:
            self.game_state.world.hover_location.render(self.map_surface)

        # Render the map surface to the map panel, centered
        surface.blit(self.map_surface, (self.map_offset_x, self.map_offset_y))
