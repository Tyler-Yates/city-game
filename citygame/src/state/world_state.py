import math
from typing import List, Set, Optional

import pygame.draw
from pygame import Surface

from citygame.src.constants.location_state_enum import LocationState
from citygame.src.constants.world_constants import DISTANCE_BETWEEN_LOCATIONS
from citygame.src.state.location_actor import Location
from citygame.src.util.locations import calculate_locations, calculate_regions, calculate_borders
from citygame.src.util.map_tile import MapTile
from citygame.src.util.maps import generate_map
from citygame.src.util.progress_bar import ProgressBar

NEIGHBOR_LINE_COLOR = [25, 25, 25, 200]


class WorldState:
    """
    Representation of a world.
    """

    def __init__(self, progress_bar: ProgressBar, map_size):
        self.map_size = map_size

        self._generate_world(progress_bar, map_size)

        self.hover_location: Optional[Location] = None

        self.locations_surface = Surface((map_size, map_size), pygame.SRCALPHA, 32)
        self.locations_surface = self.locations_surface.convert_alpha()
        self.location_roads_surface = Surface((map_size, map_size), pygame.SRCALPHA, 32)
        self.location_roads_surface = self.location_roads_surface.convert_alpha()
        self.locations_to_draw: Set[Location] = set()

        self.starting_location = self.locations[0]
        self.starting_location.set_as_starting_location()
        self.location_conquered(self.starting_location)

    def location_explored(self, location: Location):
        self.locations_to_draw.add(location)
        location.set_location_state(LocationState.EXPLORED)

        self._redraw_locations()

    def location_conquered(self, location: Location):
        self.locations_to_draw.add(location)
        location.set_location_state(LocationState.CONQUERED)

        # Now that we have conquered the location we discover the neighbors
        for neighbor in location.neighbors:
            # Only discover the location if it is hidden
            if neighbor.location_state == LocationState.HIDDEN:
                neighbor.set_location_state(LocationState.DISCOVERED)

            self.locations_to_draw.add(neighbor)

        self._redraw_locations()
        # New roads are potentially available so redraw the roads
        self._redraw_location_roads()

    def _redraw_locations(self):
        self.locations_surface = Surface((self.map_size, self.map_size), pygame.SRCALPHA, 32)
        self.locations_surface = self.location_roads_surface.convert_alpha()

        for location in self.locations_to_draw:
            location.render(self.locations_surface, hover=False)

    def _redraw_location_roads(self):
        self.location_roads_surface = Surface((self.map_size, self.map_size), pygame.SRCALPHA, 32)
        self.location_roads_surface = self.location_roads_surface.convert_alpha()
        for location in self.locations_to_draw:
            # Only conquered locations should draw roads to additional locations
            if location.location_state != LocationState.CONQUERED:
                continue

            for neighbor in location.neighbors:
                pygame.draw.aaline(
                    self.location_roads_surface, NEIGHBOR_LINE_COLOR, [location.x, location.y], [neighbor.x, neighbor.y]
                )

    def get_locations(self) -> List[Location]:
        return self.locations

    def render(self, surface: Surface):
        if self.map_size < surface.get_width() or self.map_size < surface.get_height():
            surface.fill(MapTile.get_rgb_value(MapTile.DEEP_WATER.value))

        surface_offset_x = abs(surface.get_width() - self.map_size) // 2
        surface_offset_y = abs(surface.get_height() - self.map_size) // 2

        surface.blit(self.map_surface, (surface_offset_x, surface_offset_y))

        # Draw the neighboring location lines first so the location bubbles will be drawn over them
        surface.blit(self.location_roads_surface, (surface_offset_x, surface_offset_y))

        # Draw the locations surface
        surface.blit(self.locations_surface, (surface_offset_x, surface_offset_y))

    def _generate_world(self, progress_bar: ProgressBar, map_size):
        progress_bar.set_progress(0.0, "Generating tiles...")
        self.map_tiles = generate_map(map_size, map_size)

        progress_bar.set_progress(0.3, "Generating locations...")
        location_points = calculate_locations(self.map_tiles)

        progress_bar.set_progress(0.6, "Calculating regions...")
        self.region_matrix = calculate_regions(location_points, self.map_tiles)
        self.location_to_border_points = calculate_borders(location_points, self.region_matrix)

        progress_bar.set_progress(0.8, "Calculating location graph...")
        # Create the location objects
        self.locations: List[Location] = []
        for i in range(len(location_points)):
            location_coordinates = location_points[i]
            self.locations.append(Location(i, location_coordinates[0], location_coordinates[1]))

        # Calculate neighbors for each location
        for i in range(len(self.locations)):
            current_neighbors = []
            current_location = self.locations[i]
            # TODO Generate real names
            current_location.set_name(f"Location {i}")

            x1 = current_location.x
            y1 = current_location.y

            for j in range(len(self.locations)):
                # Do not calculate a point as a neighbor of itself
                if i == j:
                    continue

                other_location = self.locations[j]
                x2 = other_location.x
                y2 = other_location.y
                distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
                if distance < (DISTANCE_BETWEEN_LOCATIONS + 1):
                    current_neighbors.append(other_location)

            # Now set the neighbors
            current_location.set_neighbors(current_neighbors)

        progress_bar.set_progress(0.8, "Saving map image...")
        # Create a map surface so that we can simply draw the surface each frame instead of each tile
        self.map_surface = Surface((map_size, map_size))
        for x in range(self.map_size):
            for y in range(self.map_size):
                tile_color = MapTile.get_rgb_value(self.map_tiles[x][y])
                pygame.draw.line(self.map_surface, tile_color, [x, y], [x, y])

        progress_bar.set_progress(1.0, "Done!")
