from typing import List

from pygame import gfxdraw, Color
from pygame.surface import Surface

from citygame.src.interfaces.actor import Actor

LOCATION_CIRCLE_RADIUS = 5


class LocationActor(Actor):
    """
    Representation of a location.
    """

    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y

        self.neighbors: List["LocationActor"] = []

    def process_input(self, events):
        pass

    def update(self, time_delta: float):
        pass

    def render(self, screen: Surface):
        gfxdraw.filled_circle(screen, self.x, self.y, LOCATION_CIRCLE_RADIUS, Color("red"))
        gfxdraw.circle(screen, self.x, self.y, LOCATION_CIRCLE_RADIUS, Color("yellow"))

    def set_neighbors(self, neighbors: List["LocationActor"]):
        self.neighbors = neighbors

    def __eq__(self, other):
        if type(other) is type(self):
            return (self.x == other.x) and (self.y == other.y)
        else:
            return False

    def __hash__(self):
        return hash((self.x, self.y))
