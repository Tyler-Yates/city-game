from typing import Optional, List

from citygame.src.constants.world_constants import DEFAULT_MAP_SIZE
from citygame.src.state.hero_actor import Hero
from citygame.src.state.world_state import WorldState


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

    def set_world(self, world):
        self.world = world

    def set_heroes(self, heroes):
        self.heroes = heroes

    def end_turn(self):
        for hero in self.heroes:
            hero.end_turn()
