from enum import Enum, auto


class SceneEnum(Enum):
    """
    Enum cataloging the various scenes in the game.
    We need this because scenes may want to transition back and forth leading to cyclical imports.
    """

    MainMenu = auto()
    Game = auto()
    GameOver = auto()
