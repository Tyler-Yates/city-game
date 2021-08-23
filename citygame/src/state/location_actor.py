import pygame.draw
from pygame.surface import Surface

from citygame.src.interfaces.actor import Actor


LOCATION_CIRCLE_RADIUS = 5.0


class LocationActor(Actor):
    """
    Representation of a location.
    """

    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y

    def process_input(self, events):
        pass

    def update(self, time_delta: float):
        pass

    def render(self, screen: Surface):
        pygame.draw.circle(screen, 'red', [self.x, self.y], LOCATION_CIRCLE_RADIUS)
        pygame.draw.circle(screen, 'yellow', [self.x, self.y], LOCATION_CIRCLE_RADIUS, width=1)
