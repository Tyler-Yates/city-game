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

    # Generate a square gradient by using the maximum of the horizontal and vertical distance from the center.
    for x in range(width):
        for y in range(height):
            gradient_matrix[x][y] = max(abs(x - center_x), abs(y - center_y))

    # Normalize the gradient values as floats between [0, 1]
    normalized_gradient_matrix = gradient_matrix / numpy.max(gradient_matrix)

    # Square each value in the gradient so that the center of the map has very low values but the outer edges maintain
    # values close to 1.
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

    # We need to ensure that we do not exceed the repeat value factoring in scale or the map could have repeated
    # sections which look odd.
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

    # Normalize the matrix values as floats between [-1, 1]
    normalized_noise_matrix = 2.0 * (noise_matrix - numpy.min(noise_matrix)) / numpy.ptp(noise_matrix) - 1

    return normalized_noise_matrix


def _calculate_tiles(noise_matrix: ndarray, water_threshold: float = -0.9) -> ndarray:
    map_tiles = numpy.zeros(noise_matrix.shape)

    # Calculate the maximum height as a reference point for the higher-level terrain
    max_height = numpy.max(noise_matrix)

    # Calculate tile threshold values once so we do not do it for every tile
    deep_water_threshold = water_threshold - 0.25
    beach_threshold = water_threshold + 0.05
    grassland_threshold = water_threshold + 0.25
    snow_threshold = max_height - 0.3
    mountain_threshold = max_height - 0.6

    for x in range(noise_matrix.shape[0]):
        for y in range(noise_matrix.shape[1]):
            # Default type
            map_tiles[x][y] = MapTile.FOREST.value

            # Lower-level terrain based on difference from the water threshold
            if noise_matrix[x][y] < deep_water_threshold:
                map_tiles[x][y] = MapTile.DEEP_WATER.value
            elif noise_matrix[x][y] < water_threshold:
                map_tiles[x][y] = MapTile.SHALLOW_WATER.value
            elif noise_matrix[x][y] < beach_threshold:
                map_tiles[x][y] = MapTile.BEACH.value
            elif noise_matrix[x][y] < grassland_threshold:
                map_tiles[x][y] = MapTile.GRASSLAND.value

            # Higher level terrain based on difference from the maximum height
            if noise_matrix[x][y] > snow_threshold:
                map_tiles[x][y] = MapTile.SNOW.value
            elif noise_matrix[x][y] > mountain_threshold:
                map_tiles[x][y] = MapTile.MOUNTAIN.value

    map_tiles = map_tiles.astype(int)
    return map_tiles


def _apply_gradient(noise_matrix: ndarray, gradient_matrix: ndarray) -> ndarray:
    resulting_matrix = numpy.zeros_like(noise_matrix)

    for x in range(noise_matrix.shape[0]):
        for y in range(noise_matrix.shape[1]):
            # Multiply by 2 to ensure the outer edges have very low values below the water threshold
            resulting_matrix[x][y] = noise_matrix[x][y] - (gradient_matrix[x][y] * 2)

    return resulting_matrix


def generate_map(width: int, height: int) -> ndarray:
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

    return map_tiles


def main():
    logging.basicConfig(level=logging.INFO)
    size = 1024
    map_tiles = generate_map(size, size)

    rgb_value_matrix = numpy.zeros(map_tiles.shape + (3,))
    for x in range(rgb_value_matrix.shape[0]):
        for y in range(rgb_value_matrix.shape[1]):
            rgb_value_matrix[x][y] = MapTile.get_rgb_value(map_tiles[x][y])

    image = Image.fromarray(rgb_value_matrix.astype("uint8"), "RGB")
    image.show()


if __name__ == "__main__":
    main()
