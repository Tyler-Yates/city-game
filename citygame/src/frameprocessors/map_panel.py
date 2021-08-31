import logging
from typing import List, TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.event import Event

from citygame.src.constants.location_state_enum import LocationState
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
        mouse_x = mouse_x - self.map_offset_x
        mouse_y = mouse_y - self.map_offset_y

        # See if any locations are the new hover location and deal with mouse actions on that location
        self.game_state.world.hover_location = None
        if 0 <= mouse_x < self.game_state.map_size and 0 <= mouse_y < self.game_state.map_size:
            hover_region = self.game_state.world.region_matrix[mouse_x][mouse_y]
            if hover_region != -1:
                hover_location = self.game_state.world.locations[hover_region]
                if hover_location.location_state != LocationState.HIDDEN:
                    self.game_state.world.hover_location = hover_location

        # Process all the events
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                # Left mouse button released
                if event.button == pygame.BUTTON_LEFT:
                    # If we have a hero selected and are hovering over a city, tell the hero to move to that location
                    if self.game_state.selected_hero and self.game_state.world.hover_location:
                        self.game_state.selected_hero.set_destination(
                            self.game_state.world.hover_location, self.game_state.world.locations
                        )
                # Right mouse button released
                if event.button == pygame.BUTTON_RIGHT:
                    # TODO remove this debug functionality
                    if self.game_state.world.hover_location:
                        self.game_state.world.location_conquered(self.game_state.world.hover_location)

        # Set the hover status now that we have redrawn everything
        if self.game_state.world.hover_location:
            self.game_state.world.hover_location.hover = True

    def update(self, time_delta: float):
        pass

    def render(self, surface: Surface):
        # Render geography first
        self.game_state.world.render_geography(self.map_surface)

        # Render roads as we want them to show up below locations
        self.game_state.world.render_roads(self.map_surface)

        # Render selected hero path if necessary
        if self.game_state.selected_hero:
            self.game_state.selected_hero.render_path(self.map_surface, pygame.Color("red"))

        # Render hover hero path if necessary
        if self.game_state.hover_hero:
            self.game_state.hover_hero.render_path(self.map_surface, pygame.Color("yellow"))

        # Render the locations above the roads
        self.game_state.world.render_locations(self.map_surface)

        # Render the hover location above the static map image
        if self.game_state.world.hover_location:
            border_points = self.game_state.world.location_to_border_points[self.game_state.world.hover_location.id]
            for border_point in border_points:
                point_tuple = (border_point[0], border_point[1])
                pygame.draw.line(self.map_surface, pygame.Color("yellow"), point_tuple, point_tuple)

            self.game_state.world.hover_location.render(self.map_surface, hover=True)

        # Render the map surface to the map panel, centered
        surface.blit(self.map_surface, (self.map_offset_x, self.map_offset_y))
