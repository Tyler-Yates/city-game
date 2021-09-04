import logging
from typing import List, TYPE_CHECKING

from pygame import Surface, Color
from pygame.event import Event

from citygame.src.interfaces.panel import Panel
from citygame.src.state.game_state import GameState
from citygame.src.util.fonts import BASIC_FONT, render_font_center_horizontal, render_lines_upper_left

if TYPE_CHECKING:
    from citygame.src.controllers.scene_controller import SceneController


BACKGROUND_COLOR = "black"

HERO_TEXT_BORDER = 5
HERO_TEXT_SPACING = 5
HERO_TEXT_SIZE = 14
HERO_TEXT_FONT = BASIC_FONT


class GeneralInformationPanel(Panel):
    """
    Panel to handle general information in the game.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController", panel_width: int, panel_height: int):
        super().__init__(game_state, scene_controller, panel_width, panel_height)
        self.log = logging.getLogger(self.__class__.__name__)
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
            render_font_center_horizontal(
                surface, f"{hover_location.name} - Level {hover_location.level}", size=24, y=20, color=Color("white")
            )

        # TODO better handling of too many events
        # Events
        lines = self.game_state.events[-10:]
        render_lines_upper_left(
            surface,
            x=0,
            y=200,
            border=HERO_TEXT_BORDER,
            spacing=HERO_TEXT_SPACING,
            lines=lines,
            size=HERO_TEXT_SIZE,
            color=Color("white"),
            font=HERO_TEXT_FONT,
        )
