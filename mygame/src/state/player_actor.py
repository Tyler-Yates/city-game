from typing import List

import pygame
from pygame import Surface
from pygame.event import Event

from mygame.src.constants.game_constants import GAME_WIDTH_PX, GAME_HEIGHT_PX
from mygame.src.interfaces.actor import Actor

PLAYER_SIZE = 20
PLAYER_OFFSET_FROM_BOTTOM = 10

PLAYER_SPEED = 240


class Player(Actor):
    def __init__(self):
        super().__init__()

        # Start the player at the center of the bottom of the screen
        self.pos_x = GAME_WIDTH_PX / 2
        self.pos_y = GAME_HEIGHT_PX - PLAYER_SIZE - PLAYER_OFFSET_FROM_BOTTOM

        self.moving_left = False
        self.moving_right = False

    def get_collision_polygon(self) -> List[List[float]]:
        point1 = [self.pos_x - (PLAYER_SIZE / 2), self.pos_y + PLAYER_SIZE]
        point2 = [self.pos_x, self.pos_y]
        point3 = [self.pos_x + (PLAYER_SIZE / 2), self.pos_y + PLAYER_SIZE]
        return [point1, point2, point3]

    def process_input(self, events: List[Event]):
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    self.moving_right = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.moving_left = True
                elif event.key == pygame.K_RIGHT:
                    self.moving_right = True

    def update(self, time_delta: float):
        if self.moving_left and (self.pos_x > PLAYER_SIZE / 2):
            self.pos_x -= PLAYER_SPEED * time_delta
        if self.moving_right and (self.pos_x < GAME_WIDTH_PX - (PLAYER_SIZE / 2)):
            self.pos_x += PLAYER_SPEED * time_delta

    def render(self, screen: Surface):
        pygame.draw.polygon(screen, "white", self.get_collision_polygon(), 0)
