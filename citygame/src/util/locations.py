import math
import random

import numpy
from PIL import Image
from numpy import ndarray

from citygame.src.util.map_tile import MapTile
from citygame.src.util.maps import generate_map


def _find_closest_valid_position(starting_location, map_tiles) -> tuple[int, int]:
    lx = starting_location[0]
    ly = starting_location[1]

    for i in range(1, map_tiles.shape[0] // 2):
        # Upper and lower row
        for x in range(lx - i, lx + i + 1):
            location = (x, ly - i)
            if _location_is_on_valid_tile(location, map_tiles):
                return location

            location = (x, ly + i)
            if _location_is_on_valid_tile(location, map_tiles):
                return location

        # Left and right columns
        for y in range(ly - i + 1, ly + i):
            location = (lx - i, y)
            if _location_is_on_valid_tile(location, map_tiles):
                return location

            location = (lx + i, y)
            if _location_is_on_valid_tile(location, map_tiles):
                return location


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

    # Add an initial seed location close to the center of the map
    starting_point = (map_tiles.shape[0] // 2, map_tiles.shape[1] // 2)
    closest_valid_starting_point = _find_closest_valid_position(starting_point, map_tiles)
    locations = [closest_valid_starting_point]

    distance_to_new_city = 50
    minimum_distance_between_cities = 30
    max_angle_iterations = 360
    angle_increment = 2.0 * math.pi / max_angle_iterations

    num_cities = 100
    for i in range(num_cities):
        location = random.choice(locations)

        angle = 2.0 * math.pi * random.random()
        for k in range(max_angle_iterations):
            angle = (angle + angle_increment) % (2.0 * math.pi)
            new_location_x = int(location[0] + math.cos(angle) * distance_to_new_city)
            new_location_y = int(location[1] - math.sin(angle) * distance_to_new_city)
            new_location = (new_location_x, new_location_y)

            if _location_is_valid(new_location, locations, map_tiles, minimum_distance_between_cities):
                print(f"Angle {angle} - Staring location {location} - New location {new_location}")
                locations.append(new_location)
                break

    for location in locations:
        map_tiles_with_cities[location[0]][location[1]] = 99
        map_tiles_with_cities[location[0]][location[1] + 1] = 99
        map_tiles_with_cities[location[0]][location[1] - 1] = 99
        map_tiles_with_cities[location[0] + 1][location[1]] = 99
        map_tiles_with_cities[location[0] - 1][location[1]] = 99

    print(f"Cities: {len(locations)}")

    return map_tiles_with_cities


def main():
    size = 1024
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
