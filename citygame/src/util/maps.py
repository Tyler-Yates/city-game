import random

import noise
import numpy
from PIL import Image
from numpy.core.records import ndarray


def _generate_noise(width: int, height: int) -> ndarray:
    noise_matrix = numpy.zeros((width, height))

    scale = 100.0
    octaves = 6
    frequency = 0.5
    amplitude = 2.0
    repeat = 1024
    base = random.randint(0, int(repeat / scale))
    print(base)

    for x in range(width):
        for y in range(height):

            noise_matrix[x][y] = noise.pnoise2(
                x / scale,
                y / scale,
                octaves=octaves,
                persistence=frequency,
                lacunarity=amplitude,
                repeatx=repeat,
                repeaty=repeat,
                base=base,
            )

    return noise_matrix


def add_color(world):
    blue = [0, 0, 0]
    green = [34, 139, 34]
    darkgreen = [0, 100, 0]
    beach = [238, 214, 175]
    snow = [255, 250, 250]
    mountain = [139, 137, 137]

    threshold = -0.2

    color_world = numpy.zeros(world.shape + (3,))
    for i in range(world.shape[0]):
        for j in range(world.shape[1]):
            if world[i][j] < threshold:
                color_world[i][j] = blue
            elif world[i][j] < threshold + 0.025:
                color_world[i][j] = beach
            elif world[i][j] < threshold + 0.25:
                color_world[i][j] = green
            elif world[i][j] < threshold + 0.6:
                color_world[i][j] = darkgreen
            elif world[i][j] < 0.7:
                color_world[i][j] = mountain
            else:
                color_world[i][j] = snow

    return color_world


def generate_world(width: int, height: int):
    noise_matrix = _generate_noise(width, height)

    color_world = add_color(noise_matrix)

    image = Image.fromarray(color_world.astype("uint8"), "RGB")
    image.show()


if __name__ == "__main__":
    generate_world(1024, 1024)
