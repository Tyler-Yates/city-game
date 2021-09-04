from typing import List, TYPE_CHECKING

from pygame import gfxdraw, Color
from pygame.surface import Surface

from citygame.src.constants.location_state_enum import LocationState
from citygame.src.constants.world_constants import LOCATION_DOT_RADIUS

if TYPE_CHECKING:
    from citygame.src.state.game_state import WorldState

LOCATION_DOT_OUTLINE_COLOR = Color("yellow")
LOCATION_DOT_OUTLINE_COLOR_HOVER = Color("purple")


class Location:
    """
    Representation of a location.
    """

    def __init__(self, location_id: int, x: int, y: int, world_state: "WorldState"):
        super().__init__()
        self.id = location_id
        self.x = x
        self.y = y
        self.world_state = world_state

        self.name = f"({x},{y})"

        self.level = 1
        self.danger_points = 100
        self.initial_danger_points = self.danger_points

        self.location_state = LocationState.HIDDEN
        self.starting_location = False

        self.neighbors: List["Location"] = []

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

    def set_neighbors(self, neighbors: List["Location"]):
        self.neighbors = neighbors

    def set_name(self, name: str):
        self.name = name

    @staticmethod
    def _get_danger_level(level: int):
        return 100 * level + 100

    def set_level(self, level: int):
        self.level = level
        self.danger_points = self._get_danger_level(level)
        self.initial_danger_points = self.danger_points

    def victory(self):
        self.danger_points -= 100

        if self.danger_points <= 0:
            self.world_state.location_conquered(self)
        elif self.danger_points < self.initial_danger_points:
            self.world_state.location_explored(self)

    def defeat(self):
        # TODO negative consequences for defeat
        pass

    def uncontested(self):
        self.danger_points = min(self.danger_points + 50, self.initial_danger_points)

        if self.danger_points == self.initial_danger_points:
            self.world_state.location_regress(self)

    def __eq__(self, other):
        if type(other) is type(self):
            return (self.id == other.id) and (self.x == other.x) and (self.y == other.y)
        else:
            return False

    def __hash__(self):
        return hash((self.id, self.x, self.y))

    def __str__(self):
        return f"{self.name} - ({self.x}, {self.y}) - {self.location_state}"

    def __repr__(self):
        return self.__str__()
