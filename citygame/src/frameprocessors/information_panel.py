import logging
from typing import List, TYPE_CHECKING

from pygame import Surface
from pygame.event import Event

from citygame.src.interfaces.panel import Panel
from citygame.src.state.game_state import GameState
from citygame.src.util.fonts import BASIC_FONT

if TYPE_CHECKING:
    from citygame.src.controllers.scene_controller import SceneController


BACKGROUND_COLOR = "black"


class GeneralInformationPanel(Panel):
    """
    Panel to handle general information in the game.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController", panel_width: int, panel_height: int):
        super().__init__(game_state, scene_controller, panel_width, panel_height)
        self.log = logging.getLogger(self.__class__.__name__)

        self.panel_width = panel_width

        self.mouse_x = None
        self.mouse_y = None

    def process_input(self, events: List[Event], mouse_x: int, mouse_y: int):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

    def update(self, time_delta: float):
        pass

    def render(self, surface: Surface):
        surface.fill(BACKGROUND_COLOR)

        BASIC_FONT.render_to(surface, [20, 100], f"({self.mouse_x}, {self.mouse_y})", "white", size=22)

        hover_location = self.game_state.world.hover_location
        if hover_location:
            text_rect = BASIC_FONT.get_rect(hover_location.name, size=32)
            text_rect.center = (surface.get_rect().center[0], 20)
            BASIC_FONT.render_to(surface, text_rect, hover_location.name, "white", size=14)
