import random
from random import randrange
from typing import List

import pygame
import pygame.gfxdraw
from pygame.surface import Surface

from mygame.src.constants.game_constants import (
    GAME_WIDTH_PX,
    MAXIMUM_ASTEROID_SIZE,
    MINIMUM_ASTEROID_SIZE,
    MAXIMUM_ASTEROID_VERTICES,
    MINIMUM_ASTEROID_VERTICES,
    ASTEROID_VARIANCE,
)
from mygame.src.interfaces.actor import Actor
from mygame.src.util.polygons import generate_polygon

BASE_SPEED = 200


class Asteroid(Actor):
    def __init__(self, pos_x: float = None, pos_y: float = None):
        super().__init__()
        if pos_x:
            self.pos_x = pos_x
        else:
            self.pos_x = randrange(0, GAME_WIDTH_PX)

        self.size = random.randint(MINIMUM_ASTEROID_SIZE, MAXIMUM_ASTEROID_SIZE)
        num_vertices = random.randint(MINIMUM_ASTEROID_VERTICES, MAXIMUM_ASTEROID_VERTICES)
        self.polygon = generate_polygon(num_vertices, self.size, ASTEROID_VARIANCE)

        if pos_y:
            self.pos_y = pos_y
        else:
            self.pos_y = -MAXIMUM_ASTEROID_SIZE * 2

        self.speed = float(MAXIMUM_ASTEROID_SIZE - MINIMUM_ASTEROID_SIZE) / self.size * BASE_SPEED

    def get_collision_polygon(self) -> List[List[float]]:
        collision_polygon_points = []
        for point in self.polygon:
            collision_polygon_points.append([self.pos_x + point[0], self.pos_y + point[1]])
        return collision_polygon_points

    def process_input(self, events):
        pass

    def update(self, time_delta: float):
        self.pos_y += self.speed * time_delta

    def render(self, screen: Surface):
        pygame.gfxdraw.aapolygon(screen, self.get_collision_polygon(), (255, 255, 255))
        pygame.gfxdraw.filled_polygon(screen, self.get_collision_polygon(), (255, 255, 255))
        pygame.gfxdraw.aapolygon(screen, self.get_collision_polygon(), (200, 200, 200))
