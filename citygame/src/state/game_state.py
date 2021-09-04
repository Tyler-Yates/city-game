import logging
import os
import pickle
from typing import Optional, List

from citygame.src.constants.location_state_enum import LocationState
from citygame.src.constants.world_constants import DEFAULT_MAP_SIZE
from citygame.src.state.hero_actor import Hero
from citygame.src.state.location_actor import Location
from citygame.src.state.world_state import WorldState
from citygame.src.util.paths import get_save_file_directory


LOG = logging.getLogger("GameState")


class GameState:
    """
    Class meant to hold the entire game state.
    """

    def __init__(self, map_size: int = DEFAULT_MAP_SIZE):
        self.map_size = map_size

        # The world state is generated async by the world creation scene
        self.world: WorldState = None

        self.heroes: List[Hero] = []
        self.selected_hero: Optional[Hero] = None
        self.hover_hero: Optional[Hero] = None

        self.events: List[str] = []

    def set_state(self, new_game_state: "GameState"):
        self.__dict__.update(new_game_state.__dict__)

    def end_turn(self):
        location_to_heroes = dict()

        for hero in self.heroes:
            hero.end_turn()

            if hero.current_location in location_to_heroes:
                location_to_heroes[hero.current_location].append(hero)
            else:
                location_to_heroes[hero.current_location] = [hero]

        for location in location_to_heroes:
            if location.location_state not in {LocationState.EXPLORED, LocationState.DISCOVERED}:
                continue

            heroes = location_to_heroes[location]
            self.battle(location, heroes)

    def battle(self, location: Location, heroes: List[Hero]):
        if len(heroes) == 0:
            return

        if len(heroes) == 1:
            message = f"{len(heroes)} hero is fighting at location {location.name}"
        else:
            message = f"{len(heroes)} heroes are fighting at location {location.name}"
        self.log_event(message)

        # TODO actual battle logic

    def log_event(self, event: str):
        self.events.append(event)

    def save(self, save_name: str):
        save_file_directory = get_save_file_directory()
        save_file_path = os.path.join(save_file_directory, f"{save_name}.sav")

        os.makedirs(os.path.dirname(save_file_path), exist_ok=True)

        with open(save_file_path, mode='wb') as save_file:
            # TODO figure out how to exclude certain traits from pickling
            pickle.dump(self, save_file)
