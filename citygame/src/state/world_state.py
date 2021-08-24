import math
from typing import List, Set

import pygame.draw
from pygame import Surface

from citygame.src.constants.location_state_enum import LocationState
from citygame.src.constants.world_constants import DISTANCE_BETWEEN_LOCATIONS
from citygame.src.state.location_actor import LocationActor
from citygame.src.util.locations import calculate_locations
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

        self.location_roads_surface = Surface((map_size, map_size), pygame.SRCALPHA, 32)
        self.location_roads_surface = self.location_roads_surface.convert_alpha()
        self.locations_to_draw: Set[LocationActor] = set()

        self.starting_location = self.locations[0]
        self.starting_location.set_as_starting_location()
        self.location_conquered(self.starting_location)

    def location_explored(self, location: LocationActor):
        self.locations_to_draw.add(location)
        location.set_location_state(LocationState.EXPLORED)

    def location_conquered(self, location: LocationActor):
        self.locations_to_draw.add(location)
        location.set_location_state(LocationState.CONQUERED)

        # Now that we have conquered the location we discover the neighbors
        for neighbor in location.neighbors:
            # Only discover the location if it is hidden
            if neighbor.location_state == LocationState.HIDDEN:
                neighbor.set_location_state(LocationState.DISCOVERED)

            self.locations_to_draw.add(neighbor)

        # New roads are potentially available so redraw the roads
        self._redraw_location_roads()

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

    def get_locations(self) -> List[LocationActor]:
        return self.locations

    def render(self, screen: Surface):
        screen.blit(self.map_surface, (0, 0))

        # Draw the neighboring location lines first so the location bubbles will be drawn over them
        screen.blit(self.location_roads_surface, (0, 0))

        # Draw each location that is at least discovered
        for location in self.locations_to_draw:
            location.render(screen)

    def _generate_world(self, progress_bar: ProgressBar, map_size):
        progress_bar.set_progress(0.0, "Generating tiles...")
        self.map_tiles = generate_map(map_size, map_size)

        progress_bar.set_progress(0.3, "Generating locations...")
        location_points = calculate_locations(self.map_tiles)

        progress_bar.set_progress(0.6, "Calculating location graph...")
        # Create the location objects
        self.locations = []
        for location_point in location_points:
            self.locations.append(LocationActor(location_point[0], location_point[1]))

        # Calculate neighbors for each location
        for i in range(len(self.locations)):
            current_neighbors = []
            current_location = self.locations[i]
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
