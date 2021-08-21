from abc import ABC
from typing import List

from pygame.surface import Surface


class Actor(ABC):
    """
    An actor is an object in the game.
    """

    def __init__(self):
        pass

    def get_collision_polygon(self) -> List[List[float]]:
        """
        Called in order to check for collisions.

        Returns:
            The collision Polygon
        """
        raise NotImplementedError("Subclass must implement.")

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
