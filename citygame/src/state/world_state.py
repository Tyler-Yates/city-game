import math
from typing import List

import pygame.draw
from pygame import Surface

from citygame.src.constants.world_constants import DISTANCE_BETWEEN_LOCATIONS
from citygame.src.state.location_actor import LocationActor
from citygame.src.util.locations import calculate_locations
from citygame.src.util.map_tile import MapTile
from citygame.src.util.maps import generate_map


class WorldState:
    """
    Representation of a world.
    """

    def __init__(self, map_size: int = 400):
        self.map_size = map_size
        self.map_tiles = generate_map(map_size, map_size)

        location_points = calculate_locations(self.map_tiles)

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

        # Create a map surface so that we can simply draw the surface each frame instead of each tile
        self.map_surface = Surface((map_size, map_size))
        for x in range(self.map_size):
            for y in range(self.map_size):
                tile_color = MapTile.get_rgb_value(self.map_tiles[x][y])
                pygame.draw.line(self.map_surface, tile_color, [x, y], [x, y])

    def get_locations(self) -> List[LocationActor]:
        return self.locations

    def render(self, screen: Surface):
        screen.blit(self.map_surface, (0, 0))

        # Draw each location
        # TODO figure out how to draw the line between each neighboring location only once
        for location in self.get_locations():
            location.render(screen)
