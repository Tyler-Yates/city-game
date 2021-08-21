import math
import random

import noise
import numpy
from PIL import Image
from numpy.core.records import ndarray


def _generate_square_gradient(width: int, height: int) -> ndarray:
    center_x = width // 2
    center_y = height // 2
    gradient_matrix = numpy.zeros((width, height))

    for x in range(width):
        for y in range(height):
            gradient_matrix[x][y] = max(abs(x - center_x), abs(y - center_y))

    normalized_gradient_matrix = gradient_matrix / numpy.max(gradient_matrix)

    # image = Image.fromarray((normalized_gradient_matrix * 255).astype("uint8"), "L")
    # image.show()

    return normalized_gradient_matrix


def _generate_noise(width: int, height: int) -> ndarray:
    noise_matrix = numpy.zeros((width, height))

    scale = 100.0
    octaves = int(math.log(width, 2))
    frequency = 0.5
    amplitude = 2.0
    repeat = 1024
    base = random.randint(0, int(repeat / scale))
    print(base)

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


def add_color(world):
    deep_water = [0, 62, 173]
    shallow_water = [9, 82, 200]
    green = [34, 139, 34]
    darkgreen = [0, 100, 0]
    beach = [238, 214, 175]
    snow = [255, 250, 250]
    mountain = [139, 137, 137]

    water_threshold = -0.9
    max_height = numpy.max(world)

    color_world = numpy.zeros(world.shape + (3,))
    for i in range(world.shape[0]):
        for j in range(world.shape[1]):

            # Default type
            color_world[i][j] = darkgreen

            if world[i][j] < water_threshold - 0.25:
                color_world[i][j] = deep_water
            elif world[i][j] < water_threshold:
                color_world[i][j] = shallow_water
            elif world[i][j] < water_threshold + 0.05:
                color_world[i][j] = beach
            elif world[i][j] < water_threshold + 0.25:
                color_world[i][j] = green

            if world[i][j] > max_height - 0.2:
                color_world[i][j] = snow
            elif world[i][j] > max_height - 0.5:
                color_world[i][j] = mountain

    return color_world


def _apply_gradient(noise_matrix: ndarray, gradient_matrix: ndarray) -> ndarray:
    resulting_matrix = numpy.zeros_like(noise_matrix)

    for x in range(noise_matrix.shape[0]):
        for y in range(noise_matrix.shape[1]):
            resulting_matrix[x][y] = noise_matrix[x][y] - (gradient_matrix[x][y] * 2)

    return resulting_matrix


def generate_world(width: int, height: int):
    noise_matrix = _generate_noise(width, height)
    square_gradient_matrix = _generate_square_gradient(width, height)

    gradient_applied_matrix = _apply_gradient(noise_matrix, square_gradient_matrix)

    color_world = add_color(gradient_applied_matrix)

    image = Image.fromarray(color_world.astype("uint8"), "RGB")
    image.show()


if __name__ == "__main__":
    size = 1024
    generate_world(size, size)
