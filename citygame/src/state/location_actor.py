from typing import List

from pygame import gfxdraw, Color
from pygame.surface import Surface

from citygame.src.constants.location_state_enum import LocationState
from citygame.src.constants.world_constants import LOCATION_DOT_RADIUS

LOCATION_DOT_OUTLINE_COLOR = Color("yellow")
LOCATION_DOT_OUTLINE_COLOR_HOVER = Color("purple")


class LocationActor:
    """
    Representation of a location.
    """

    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y

        self.name = f"({x},{y})"

        self.location_state = LocationState.HIDDEN
        self.starting_location = False

        self.neighbors: List["LocationActor"] = []

    def render(self, surface: Surface, hover: bool):
        dot_color = LocationState.get_rgb_color(self.location_state)
        gfxdraw.filled_circle(surface, self.x, self.y, LOCATION_DOT_RADIUS, dot_color)

        outline_color = LOCATION_DOT_OUTLINE_COLOR
        if hover:
            outline_color = LOCATION_DOT_OUTLINE_COLOR_HOVER
        gfxdraw.circle(surface, self.x, self.y, LOCATION_DOT_RADIUS, outline_color)

    def set_as_starting_location(self):
        self.starting_location = True
        self.location_state = LocationState.CONQUERED

    def set_location_state(self, location_state: LocationState):
        self.location_state = location_state

    def set_neighbors(self, neighbors: List["LocationActor"]):
        self.neighbors = neighbors

    def set_name(self, name: str):
        self.name = name

    def __eq__(self, other):
        if type(other) is type(self):
            return (self.x == other.x) and (self.y == other.y)
        else:
            return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y}) - {self.location_state}"

    def __repr__(self):
        return self.__str__()
