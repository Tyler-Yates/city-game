from typing import List, TYPE_CHECKING

from pygame import Surface
from pygame.event import Event

from citygame.src.interfaces.scene import Scene
from citygame.src.state.game_state import GameState

if TYPE_CHECKING:
    from citygame.src.controllers.scene_controller import SceneController

BACKGROUND_COLOR = (0, 0, 0)


class GameOverScene(Scene):
    """
    GameOverScene
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController"):
        super().__init__(game_state, scene_controller)

    def process_input(self, events: List[Event]):
        pass

    def update(self, time_delta: float):
        pass

    def render(self, screen: Surface):
        screen.fill(BACKGROUND_COLOR)
