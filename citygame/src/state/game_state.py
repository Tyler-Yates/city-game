from citygame.src.state.world_state import WorldState


class GameState:
    """
    Class meant to hold the entire game state.
    """

    def __init__(self, map_size: int = 300):
        self.map_size = map_size

        # The world state is generated async by the world creation scene
        self.world: WorldState = None

        self.heroes = []

    def set_world(self, world):
        self.world = world

    def set_heroes(self, heroes):
        self.heroes = heroes
