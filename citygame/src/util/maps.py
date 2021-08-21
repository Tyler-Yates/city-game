import logging
import math
import random

import noise
import numpy
from PIL import Image
from numpy.core.records import ndarray

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
    deep_water = [0, 62, 173]
    shallow_water = [9, 82, 200]
    green = [34, 139, 34]
    darkgreen = [0, 100, 0]
    beach = [238, 214, 175]
    snow = [255, 250, 250]
    mountain = [139, 137, 137]

    water_threshold = -0.9
    max_height = numpy.max(noise_matrix)

    tile_matrix = numpy.zeros(noise_matrix.shape + (3,))
    for i in range(noise_matrix.shape[0]):
        for j in range(noise_matrix.shape[1]):

            # Default type
            tile_matrix[i][j] = darkgreen

            if noise_matrix[i][j] < water_threshold - 0.25:
                tile_matrix[i][j] = deep_water
            elif noise_matrix[i][j] < water_threshold:
                tile_matrix[i][j] = shallow_water
            elif noise_matrix[i][j] < water_threshold + 0.05:
                tile_matrix[i][j] = beach
            elif noise_matrix[i][j] < water_threshold + 0.25:
                tile_matrix[i][j] = green

            if noise_matrix[i][j] > max_height - 0.3:
                tile_matrix[i][j] = snow
            elif noise_matrix[i][j] > max_height - 0.6:
                tile_matrix[i][j] = mountain

    return tile_matrix


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
    color_world = _calculate_tiles(gradient_applied_matrix)
    LOG.info("Completed generation")

    image = Image.fromarray(color_world.astype("uint8"), "RGB")
    image.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    size = 1024
    generate_world(size, size)
