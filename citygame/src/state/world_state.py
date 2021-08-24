import math
from typing import List

import pygame.draw
from pygame import Surface

from citygame.src.constants.world_constants import DISTANCE_BETWEEN_LOCATIONS
from citygame.src.state.location_actor import LocationActor
from citygame.src.util.locations import calculate_locations
from citygame.src.util.map_tile import MapTile
from citygame.src.util.maps import generate_map
from citygame.src.util.progress_bar import ProgressBar

NEIGHBOR_LINE_COLOR = [25, 25, 25, 50]


class WorldState:
    """
    Representation of a world.
    """

    def __init__(self, progress_bar: ProgressBar, map_size: int = 400):
        progress_bar.set_progress(0.0, "Generating tiles...")
        self.map_size = map_size
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

        progress_bar.set_progress(0.7, "Saving map image...")
        # Create a map surface so that we can simply draw the surface each frame instead of each tile
        self.map_surface = Surface((map_size, map_size))
        for x in range(self.map_size):
            for y in range(self.map_size):
                tile_color = MapTile.get_rgb_value(self.map_tiles[x][y])
                pygame.draw.line(self.map_surface, tile_color, [x, y], [x, y])

        progress_bar.set_progress(0.9, "Saving location graph lines...")
        # Save the neighbor lines so we don't have to calculate them each frame
        self.neighbor_lines = set()
        for location in self.locations:
            for neighbor in location.neighbors:
                sorted_point_list = sorted([(location.x, location.y), (neighbor.x, neighbor.y)])
                self.neighbor_lines.add((sorted_point_list[0], sorted_point_list[1]))

        progress_bar.set_progress(1.0, "Done!")

    def get_locations(self) -> List[LocationActor]:
        return self.locations

    def render(self, screen: Surface):
        screen.blit(self.map_surface, (0, 0))

        # Draw the neighboring location lines first so the location bubbles will be drawn over them
        # TODO draw lines once to surface so we don't have to iterate each frame
        for neighbor_line in self.neighbor_lines:
            point1 = neighbor_line[0]
            point2 = neighbor_line[1]
            pygame.draw.aaline(screen, NEIGHBOR_LINE_COLOR, [point1[0], point1[1]], [point2[0], point2[1]])

        # Draw each location
        for location in self.get_locations():
            location.render(screen)
