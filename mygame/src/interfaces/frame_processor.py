from abc import ABC

# Avoid cyclic imports since we only want these for type checking
from typing import TYPE_CHECKING

from pygame.surface import Surface

from mygame.src.state.game_state import GameState

if TYPE_CHECKING:
    from mygame.src.controllers.scene_controller import SceneController


class FrameProcessor(ABC):
    """
    A FrameProcessor is meant to process information each frame.

    This is an abstract class and should be implemented by other classes.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController"):
        self.game_state = game_state
        self.scene_controller = scene_controller

    def process_input(self, events):
        """
        Called every frame by the game director.
        This method should process any input events that have come in for this frame.

        Args:
            events: The input events
        """
        raise NotImplementedError("Subclass must implement.")

    def update(self, time_delta: float):
        """
        Called every frame by the game director after `process_input`.
        This method should update any game state.

        Args:
            time_delta: A float representing the fraction of a second that has elapsed since the previous frame.
        """
        raise NotImplementedError("Subclass must implement.")

    def render(self, screen: Surface):
        """
        Called every frame by the game director after `update`.

        Args:
            screen: The Surface to render to
        """
        raise NotImplementedError("Subclass must implement.")
