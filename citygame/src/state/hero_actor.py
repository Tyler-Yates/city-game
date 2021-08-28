import uuid

from pygame import Color
from pygame.surface import Surface

from citygame.src.interfaces.actor import Actor
from citygame.src.state.location_actor import LocationActor
from citygame.src.util.fonts import render_font_center


class Hero(Actor):
    """
    Representation of a hero.
    """

    def __init__(self, starting_location: LocationActor):
        super().__init__()

        self.id = str(uuid.uuid4())
        self.level = 1

        # TODO Hero name generation
        self.name = "Hero Name"

        self.current_location = starting_location

    def process_input(self, events):
        pass

    def update(self, time_delta: float):
        pass

    def render(self, surface: Surface):
        render_font_center(surface, f"{self.name} Lv. {self.level}", 14, Color("white"))

    def __eq__(self, other):
        if type(other) is type(self):
            return self.id == other.id
        else:
            return False

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"({self.name} - Lv. {self.level}"

    def __repr__(self):
        return self.__str__()
