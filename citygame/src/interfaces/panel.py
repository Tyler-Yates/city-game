from abc import ABC

# Avoid cyclic imports since we only want these for type checking
from typing import TYPE_CHECKING

from pygame.surface import Surface

from citygame.src.state.game_state import GameState

if TYPE_CHECKING:
    from citygame.src.controllers.scene_controller import SceneController


class Panel(ABC):
    """
    A Panel is meant to represent a part of the screen.
    This allows the main scene controller to delegate logic to panels.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController", panel_width: int, panel_height: int):
        self.game_state = game_state
        self.scene_controller = scene_controller
        self.panel_width = panel_width
        self.panel_height = panel_height

    def process_input(self, events, mouse_x: int, mouse_y: int):
        """
        Called every frame by the game director.
        This method should process any input events that have come in for this frame.

        Args:
            events: The input events
            mouse_x: The x position of the mouse relative to the upper-left of the panel
            mouse_y: The y position of the mouse relative to the upper-left of the panel
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

    def render(self, panel_surface: Surface):
        """
        Called every frame. The panel should draw on its surface.

        Args:
            panel_surface: The Surface to render to
        """
        raise NotImplementedError("Subclass must implement.")
