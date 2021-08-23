from typing import List

import pygame.draw
from pygame import Surface

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

        self.locations = []
        for location_point in location_points:
            self.locations.append(LocationActor(location_point[0], location_point[1]))

        self.map_surface = Surface((map_size, map_size))
        for x in range(self.map_size):
            for y in range(self.map_size):
                tile_color = MapTile.get_rgb_value(self.map_tiles[x][y])
                pygame.draw.line(self.map_surface, tile_color, [x, y], [x, y])

    def get_locations(self) -> List[LocationActor]:
        return self.locations

    def render(self, screen: Surface):
        screen.blit(self.map_surface, (0, 0))
