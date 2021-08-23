from citygame.src.state.world_state import WorldState


class GameState:
    """
    Class meant to hold the entire game state.
    """

    def __init__(self):
        self.world: WorldState = None

    def reset(self):
        """
        Method to be called whenever the game state should be reset, for example starting a new game.
        """
        self.world = WorldState()
