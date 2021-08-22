import math
import random

import numpy
from PIL import Image
from numpy import ndarray

from citygame.src.util.map_tile import MapTile
from citygame.src.util.maps import generate_map


def _location_is_too_close_to_existing_locations(new_location, existing_locations, minimum_distance: int) -> bool:
    x1 = new_location[0]
    y1 = new_location[1]

    for existing_location in existing_locations:
        x2 = existing_location[0]
        y2 = existing_location[1]
        distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

        if distance < minimum_distance:
            return True

    return False


def _location_is_on_valid_tile(location, map_tiles: ndarray) -> bool:
    return MapTile.is_buildable_tile(map_tiles[location[0]][location[1]])


def _location_is_valid(
    location, existing_locations, map_tiles: ndarray, minimum_distance_between_locations: int
) -> bool:
    return _location_is_on_valid_tile(location, map_tiles) and (
        not _location_is_too_close_to_existing_locations(
            location, existing_locations, minimum_distance_between_locations
        )
    )


def place_locations(map_tiles: ndarray) -> ndarray:
    map_tiles_with_cities = numpy.matrix.copy(map_tiles)

    # Add an initial seed location at the center of the map
    locations = [(map_tiles.shape[0] // 2, map_tiles.shape[1] // 2)]

    distance_between_cities = 50

    for i in range(20):
        location = random.choice(locations)

        for k in range(100):
            angle = 2 * math.pi * random.random()
            new_location_x = int(location[0] + math.cos(angle) * distance_between_cities)
            new_location_y = int(location[1] + math.sin(angle) * distance_between_cities)
            new_location = (new_location_x, new_location_y)

            if _location_is_valid(new_location, locations, map_tiles, distance_between_cities):
                locations.append(new_location)

    for location in locations:
        map_tiles_with_cities[location[0]][location[1]] = 99

    return map_tiles_with_cities


def main():
    size = 500
    map_tiles = generate_map(size, size)
    map_tiles_with_cities = place_locations(map_tiles)

    rgb_value_matrix = numpy.zeros(map_tiles_with_cities.shape + (3,))
    for x in range(rgb_value_matrix.shape[0]):
        for y in range(rgb_value_matrix.shape[1]):
            rgb_value_matrix[x][y] = MapTile.get_rgb_value(map_tiles_with_cities[x][y])

    image = Image.fromarray(rgb_value_matrix.astype("uint8"), "RGB")
    image.show()


if __name__ == "__main__":
    main()
