import math
import random
import uuid
from typing import List, Optional, TYPE_CHECKING

import pygame.draw_py
from pygame import Color
from pygame.surface import Surface

from citygame.src.constants.location_state_enum import LocationState
from citygame.src.interfaces.actor import Actor
from citygame.src.state.location_actor import Location
from citygame.src.util.fonts import render_font_center

if TYPE_CHECKING:
    from citygame.src.state.game_state import GameState


class Hero(Actor):
    """
    Representation of a hero.
    """

    def __init__(self, starting_location: Location, game_state: "GameState"):
        super().__init__()

        self.game_state = game_state

        self.id = str(uuid.uuid4())
        self.level = 1

        self.hp = 10
        self.max_hp = 10

        # TODO Hero name generation
        self.name = f"Hero {random.randint(0, 99)}"

        self.current_location = starting_location

        self.move_path: List[Location] = []
        self.destination: Optional[Location] = None

    def process_input(self, events):
        pass

    def update(self, time_delta: float):
        pass

    def render(self, surface: Surface):
        render_font_center(surface, f"{self.name} Lv. {self.level}", 14, Color("white"))

    def render_path(self, surface: Surface, color: Color):
        if self.destination:
            current_location = self.current_location
            for path_location in self.move_path:
                pygame.draw.line(
                    surface, color, (current_location.x, current_location.y), (path_location.x, path_location.y)
                )
                current_location = path_location

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

    def set_destination(self, destination: Location, locations: List[Location]):
        if destination == self.current_location:
            return

        self.move_path = self._calculate_path_to_destination(destination, locations)
        self.destination = destination

    def end_turn(self):
        if self.destination:
            self.move()

        # TODO battles and other logic

    def move(self):
        # If the first element in the move path is the current location, get rid of it
        if next(iter(self.move_path), None) == self.current_location:
            self.move_path.pop(0)

        # Sanity check
        if len(self.move_path) == 0:
            self.destination = None
            return

        # Pop from the path since we are moving to that location
        next_location = self.move_path.pop(0)
        self.current_location = next_location
        self.game_state.log_event(f"Hero {self.name} moved to {self.current_location.name}")

        if self.destination == self.current_location:
            self.destination = None
            self.move_path = []

    def _calculate_path_to_destination(self, destination: Location, locations: List[Location]) -> List[Location]:
        location_set = set()

        location_to_distance = dict()
        location_to_previous_location = dict()
        for location in locations:
            # Do not consider hidden locations
            if location.location_state == LocationState.HIDDEN:
                continue

            location_to_distance[location] = math.inf
            location_to_previous_location[location] = None
            location_set.add(location)

        location_to_distance[self.current_location] = 0

        while len(location_set) > 0:
            minimum_distance_location = next(iter(location_set))
            minimum_distance = location_to_distance[minimum_distance_location]
            for location in location_set:
                if location_to_distance[location] < minimum_distance:
                    minimum_distance_location = location
                    minimum_distance = location_to_distance[location]

            location_set.remove(minimum_distance_location)

            # Break out of the loop if we have reached our destination
            if minimum_distance_location == destination:
                break

            # Heroes can only move through conquered locations bue we should always be able to move from the current
            # location regardless of its state
            if (
                minimum_distance_location.location_state == LocationState.CONQUERED
                or minimum_distance_location == self.current_location
            ):
                for neighbor in minimum_distance_location.neighbors:
                    # Do not consider hidden locations
                    if neighbor.location_state == LocationState.HIDDEN:
                        continue

                    # TODO calculate actual distance between location and its neighbor based on geography
                    alt = location_to_distance[minimum_distance_location] + 1
                    if alt < location_to_distance[neighbor]:
                        location_to_distance[neighbor] = alt
                        location_to_previous_location[neighbor] = minimum_distance_location

        # Build up the path by grabbing the previous location starting with the destination
        path = []
        location_pointer = destination
        if location_to_previous_location[destination] or destination == self.current_location:
            while location_pointer:
                # We don't need to add the current location to the path as we are already there
                if location_pointer == self.current_location:
                    break

                path.insert(0, location_pointer)
                location_pointer = location_to_previous_location[location_pointer]

        return path

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
