from citygame.src.state.world_state import WorldState


class GameState:
    """
    Class meant to hold the entire game state.
    """

    def __init__(self, map_size: int = 400):
        self.map_size = map_size
        self.world: WorldState = None

    def reset(self):
        """
        Method to be called whenever the game state should be reset, for example starting a new game.
        """
        pass
