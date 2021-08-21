import logging
import math
import random

import noise
import numpy
from PIL import Image
from numpy.core.records import ndarray

from citygame.src.util.map_tile import MapTile

LOG = logging.getLogger("maps")


def _generate_square_gradient(width: int, height: int) -> ndarray:
    center_x = width // 2
    center_y = height // 2
    gradient_matrix = numpy.zeros((width, height))

    for x in range(width):
        for y in range(height):
            gradient_matrix[x][y] = max(abs(x - center_x), abs(y - center_y))

    normalized_gradient_matrix = gradient_matrix / numpy.max(gradient_matrix)
    normalized_gradient_matrix = numpy.square(normalized_gradient_matrix)

    # image = Image.fromarray((normalized_gradient_matrix * 255).astype("uint8"), "L")
    # image.show()

    return normalized_gradient_matrix


def _generate_noise(width: int, height: int) -> ndarray:
    noise_matrix = numpy.zeros((width, height))

    scale = 100.0
    octaves = int(math.log(width, 2))
    frequency = 0.5
    amplitude = 2.0
    repeat = 1048576

    base = random.randint(0, int(repeat / scale))
    LOG.info(f"Map seed: {base}")

    for x in range(width):
        for y in range(height):
            noise_matrix[x][y] = noise._simplex.noise2(
                x / scale,
                y / scale,
                octaves=octaves,
                persistence=frequency,
                lacunarity=amplitude,
                repeatx=repeat,
                repeaty=repeat,
                base=base,
            )

    # Normalize between -1 and 1
    normalized_noise_matrix = 2.0 * (noise_matrix - numpy.min(noise_matrix)) / numpy.ptp(noise_matrix) - 1

    return normalized_noise_matrix


def _calculate_tiles(noise_matrix: ndarray) -> ndarray:
    water_threshold = -0.9
    max_height = numpy.max(noise_matrix)

    map_tiles = numpy.zeros(noise_matrix.shape)

    for x in range(noise_matrix.shape[0]):
        for j in range(noise_matrix.shape[1]):

            # Default type
            map_tiles[x][j] = MapTile.FOREST.value

            if noise_matrix[x][j] < water_threshold - 0.25:
                map_tiles[x][j] = MapTile.DEEP_WATER.value
            elif noise_matrix[x][j] < water_threshold:
                map_tiles[x][j] = MapTile.SHALLOW_WATER.value
            elif noise_matrix[x][j] < water_threshold + 0.05:
                map_tiles[x][j] = MapTile.BEACH.value
            elif noise_matrix[x][j] < water_threshold + 0.25:
                map_tiles[x][j] = MapTile.GRASSLAND.value

            if noise_matrix[x][j] > max_height - 0.3:
                map_tiles[x][j] = MapTile.SNOW.value
            elif noise_matrix[x][j] > max_height - 0.6:
                map_tiles[x][j] = MapTile.MOUNTAIN.value

    map_tiles = map_tiles.astype(int)
    return map_tiles


def _apply_gradient(noise_matrix: ndarray, gradient_matrix: ndarray) -> ndarray:
    resulting_matrix = numpy.zeros_like(noise_matrix)

    for x in range(noise_matrix.shape[0]):
        for y in range(noise_matrix.shape[1]):
            resulting_matrix[x][y] = noise_matrix[x][y] - (gradient_matrix[x][y] * 2)

    return resulting_matrix


def generate_world(width: int, height: int):
    LOG.info(f"Creating new map with dimensions {width}x{height}")
    LOG.info("Generating noise...")
    noise_matrix = _generate_noise(width, height)
    LOG.info("Generating gradient...")
    square_gradient_matrix = _generate_square_gradient(width, height)
    LOG.info("Applying gradient...")
    gradient_applied_matrix = _apply_gradient(noise_matrix, square_gradient_matrix)
    LOG.info("Calculating tiles...")
    map_tiles = _calculate_tiles(gradient_applied_matrix)
    LOG.info("Completed generation")

    # If you want to save the map in a compressed form:
    # numpy.savez_compressed("map", map_tiles, fmt='%i')

    rgb_value_matrix = numpy.zeros(map_tiles.shape + (3,))
    for x in range(rgb_value_matrix.shape[0]):
        for y in range(rgb_value_matrix.shape[1]):
            rgb_value_matrix[x][y] = MapTile.get_rgb_value(map_tiles[x][y])

    image = Image.fromarray(rgb_value_matrix.astype("uint8"), "RGB")
    image.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    size = 1024
    generate_world(size, size)
