import logging
import math
import random

import numpy
from PIL import Image
from numpy import ndarray

from citygame.src.constants.world_constants import DISTANCE_BETWEEN_LOCATIONS, MINIMUM_DISTANCE_BETWEEN_LOCATIONS
from citygame.src.util.map_tile import MapTile
from citygame.src.util.maps import generate_map

LOG = logging.getLogger("maps")


def _find_closest_valid_position(starting_location, map_tiles) -> tuple[int, int]:
    lx = starting_location[0]
    ly = starting_location[1]

    for i in range(1, map_tiles.shape[0] // 2 - 2):
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
    # Do not check locations outside of the map
    if location[0] < 0 or location[0] >= map_tiles.shape[0]:
        return False
    if location[1] < 0 or location[1] >= map_tiles.shape[1]:
        return False

    tile_valid = _location_is_on_valid_tile(location, map_tiles)
    distance_valid = not _location_is_too_close_to_existing_locations(
        location, existing_locations, minimum_distance_between_locations
    )
    return tile_valid and distance_valid


def _calculate_regions(locations: list[tuple[int, int]], map_tiles: ndarray):
    region_matrix = numpy.zeros_like(map_tiles)
    region_matrix.fill(-1)

    for i in range(len(locations)):
        location = locations[i]
        region_matrix[location[0]][location[1]] = i

    points_processed = set()
    while True:
        points_claimed = 0

        points_to_process = set()
        for x in range(region_matrix.shape[0]):
            for y in range(region_matrix.shape[1]):
                if (x, y) in points_processed:
                    continue

                region = region_matrix[x][y]
                if region != -1:
                    points_to_process.add((x, y, region))

        for point in points_to_process:
            points_processed.add(point)
            x = point[0]
            y = point[1]
            region = point[2]
            points_claimed += _claim_point_if_valid(region, region_matrix, x - 1, y, map_tiles)
            points_claimed += _claim_point_if_valid(region, region_matrix, x + 1, y, map_tiles)
            points_claimed += _claim_point_if_valid(region, region_matrix, x, y - 1, map_tiles)
            points_claimed += _claim_point_if_valid(region, region_matrix, x, y + 1, map_tiles)

        if points_claimed == 0:
            break

    return region_matrix


def _claim_point_if_valid(region: int, regions: ndarray, x: int, y: int, map_tiles: ndarray) -> int:
    if x < 0 or y < 0 or x >= map_tiles.shape[0] or y >= map_tiles.shape[1]:
        return 0

    if regions[x][y] != -1:
        return 0

    if not MapTile.is_land(map_tiles[x][y]):
        return 0

    regions[x][y] = region
    return 1


def calculate_locations(map_tiles: ndarray) -> list[tuple[int, int]]:
    LOG.info("Generating locations...")

    # Add an initial seed location close to the center of the map.
    starting_point = (map_tiles.shape[0] // 2, map_tiles.shape[1] // 2)
    closest_valid_starting_point = _find_closest_valid_position(starting_point, map_tiles)
    locations = [closest_valid_starting_point]

    # Some locations may be in a place where no further locations can be added from.
    # Those locations should no longer be used as seeds to generate new locations.
    seed_locations = {closest_valid_starting_point}

    # Constants to use when placing locations
    max_angle_iterations = 360
    angle_increment = 2.0 * math.pi / max_angle_iterations

    # Keep generating locations as long as we have seeds to use
    while len(seed_locations) > 0:
        # Pick a random seed location to use as a start point
        seed_location = random.choice(tuple(seed_locations))
        seed_x = seed_location[0]
        seed_y = seed_location[1]

        # Start at a random angle and progressively add to the angle until we find a location that is valid or we run
        # out of attempts.
        angle = 2.0 * math.pi * random.random()
        placed_new_location = False
        for k in range(max_angle_iterations):
            angle = (angle + angle_increment) % (2.0 * math.pi)
            new_location_x = int(seed_x + math.cos(angle) * DISTANCE_BETWEEN_LOCATIONS)
            new_location_y = int(seed_y - math.sin(angle) * DISTANCE_BETWEEN_LOCATIONS)
            new_location = (new_location_x, new_location_y)

            if _location_is_valid(new_location, locations, map_tiles, MINIMUM_DISTANCE_BETWEEN_LOCATIONS):
                locations.append(new_location)
                seed_locations.add(new_location)
                placed_new_location = True
                # We found a valid location so we don't need to continue adding to the angle
                break

        # If we did not find a valid location then this seed location is no longer able to place new locations.
        # Remove it from the seed set so we don't try to use it again.
        if not placed_new_location:
            seed_locations.remove(seed_location)

    LOG.info(f"Locations placed: {len(locations)}")

    _calculate_regions(locations, map_tiles)

    return locations


def main():
    size = 125
    map_tiles = generate_map(size, size)

    LOG.info("Calculating locations...")
    locations = calculate_locations(map_tiles)

    for location in locations:
        map_tiles[location[0]][location[1]] = 99
        map_tiles[location[0]][location[1] + 1] = 99
        map_tiles[location[0]][location[1] - 1] = 99
        map_tiles[location[0] + 1][location[1]] = 99
        map_tiles[location[0] - 1][location[1]] = 99

    rgb_value_matrix = numpy.zeros(map_tiles.shape + (3,))
    for x in range(rgb_value_matrix.shape[0]):
        for y in range(rgb_value_matrix.shape[1]):
            rgb_value_matrix[x][y] = MapTile.get_rgb_value(map_tiles[x][y])

    image = Image.fromarray(rgb_value_matrix.astype("uint8"), "RGB")
    image.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
