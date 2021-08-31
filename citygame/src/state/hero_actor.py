import random
import uuid
from typing import List, Optional

from pygame import Color
from pygame.surface import Surface

from citygame.src.interfaces.actor import Actor
from citygame.src.state.location_actor import Location
from citygame.src.util.fonts import render_font_center


class Hero(Actor):
    """
    Representation of a hero.
    """

    def __init__(self, starting_location: Location):
        super().__init__()

        self.id = str(uuid.uuid4())
        self.level = 1

        self.hp = 10
        self.max_hp = 10

        # TODO Hero name generation
        self.name = f"Hero {random.randint(0, 99)}"

        self.current_location = starting_location
        self.destination: Optional[Location] = None

    def process_input(self, events):
        pass

    def update(self, time_delta: float):
        pass

    def render(self, surface: Surface):
        render_font_center(surface, f"{self.name} Lv. {self.level}", 14, Color("white"))

    def get_destination(self) -> str:
        if self.destination:
            return self.destination.name
        return "None"

    def get_full_information(self) -> List[str]:
        return [
            f"{self.name}",
            f"Level {self.level}",
            f"HP {self.hp}/{self.max_hp}",
            "",
            f"Location: {self.current_location.name}",
            f"Destination: {self.get_destination()}",
        ]

    def set_destination(self, destination: Location):
        if destination == self.current_location:
            return

        self.destination = destination

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
