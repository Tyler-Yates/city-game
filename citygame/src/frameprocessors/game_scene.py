import logging
import math
from typing import List, TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.event import Event

from citygame.src.constants.world_constants import LOCATION_DOT_RADIUS
from citygame.src.interfaces.scene import Scene
from citygame.src.state.game_state import GameState

if TYPE_CHECKING:
    from citygame.src.controllers.scene_controller import SceneController


BACKGROUND_COLOR = "black"


class GameScene(Scene):
    """
    Scene that handles actual gameplay.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController"):
        super().__init__(game_state, scene_controller)

        self.log = logging.getLogger(self.__class__.__name__)

    def process_input(self, events: List[Event]):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

        for location in self.game_state.world.locations:
            distance = math.sqrt(math.pow(location.x - mouse_x, 2) + math.pow(location.y - mouse_y, 2))
            if distance <= LOCATION_DOT_RADIUS:
                location.hover = True

                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.game_state.world.location_conquered(location)
            else:
                location.hover = False

    def update(self, time_delta: float):
        pass

    def render(self, screen: Surface):
        screen.fill(BACKGROUND_COLOR)

        self.game_state.world.render(screen)
