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
        self.hover_hero: Optional[Hero] = None

        self.events: List[str] = []

    def set_state(self, new_game_state: "GameState"):
        self.__dict__.update(new_game_state.__dict__)

    def end_turn(self):
        for hero in self.heroes:
            hero.end_turn()

    def log_event(self, event: str):
        self.events.append(event)
