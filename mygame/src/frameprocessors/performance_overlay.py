from typing import List, TYPE_CHECKING

import pygame
from pygame.event import Event
from pygame.surface import Surface

from mygame.src.interfaces.overlay import Overlay
from mygame.src.state.game_state import GameState
from mygame.src.util.fonts import BASIC_FONT

if TYPE_CHECKING:
    from mygame.src.controllers.scene_controller import SceneController

TOGGLE_HOTKEY = pygame.K_F12

# The start of the game may have some hitches so wait a bit before recording
RECORDING_DELAY = 10

PERFORMANCE_TEXT_SIZE = 14


class PerformanceOverlay(Overlay):
    """
    Displays performance information for the game.

    This information can be toggled by pressing F12.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController"):
        super().__init__(game_state, scene_controller)

        self.show_fps = True
        self.num_updates = 0
        self.maximum_time_delta = 0
        self.time_delta = 0

    def process_input(self, events: List[Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == TOGGLE_HOTKEY:
                    self.show_fps = not self.show_fps

    def update(self, time_delta: float):
        self.num_updates += 1
        self.time_delta = int(time_delta * 1000)
        if self.num_updates > RECORDING_DELAY and self.time_delta > self.maximum_time_delta:
            self.maximum_time_delta = self.time_delta

    def render(self, screen: Surface):
        if self.show_fps:
            text = f"Frametime: {self.time_delta} | Maximum Frametime: {self.maximum_time_delta}"
            text_rect = BASIC_FONT.get_rect(text, size=PERFORMANCE_TEXT_SIZE)
            text_rect.topright = (screen.get_width() - 5, 5)

            BASIC_FONT.render_to(screen, text_rect, text, "red", size=PERFORMANCE_TEXT_SIZE)
