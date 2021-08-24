from concurrent.futures import ThreadPoolExecutor
from typing import List, TYPE_CHECKING

from pygame import Surface
from pygame.event import Event

from citygame.src.constants.scene_enum import SceneEnum
from citygame.src.interfaces.scene import Scene
from citygame.src.state.game_state import GameState
from citygame.src.state.world_state import WorldState
from citygame.src.util.fonts import BASIC_FONT
from citygame.src.util.progress_bar import ProgressBar

if TYPE_CHECKING:
    from citygame.src.controllers.scene_controller import SceneController

BACKGROUND_COLOR = (0, 0, 0)

TEXT_SIZE = 48


class WorldCreationScene(Scene):
    """
    Scene while a new map is created.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController"):
        super().__init__(game_state, scene_controller)

        self.progress_bar = ProgressBar()

        # We only need one thread running in the background to generate the world
        self.executor_pool = ThreadPoolExecutor(1)
        self.map_generation_future = self.executor_pool.submit(
            self.generate_new_world_state, self.progress_bar, self.game_state.map_size
        )

    @staticmethod
    def generate_new_world_state(progress_bar: ProgressBar, map_size: int) -> WorldState:
        return WorldState(progress_bar, map_size=map_size)

    def process_input(self, events: List[Event]):
        pass

    def update(self, time_delta: float):
        # If the world is done generating we can update the game state and move on to the game scene
        if self.map_generation_future.done():
            self.game_state.world = self.map_generation_future.result()
            self.executor_pool.shutdown()
            self.scene_controller.change_active_scene(SceneEnum.Game)

    def render(self, screen: Surface):
        screen.fill(BACKGROUND_COLOR)

        progress = int(self.progress_bar.progress * 100)
        progress_text = f"{progress}%"
        progress_text_rect = BASIC_FONT.get_rect(progress_text, size=TEXT_SIZE)
        progress_text_rect.center = screen.get_rect().center
        BASIC_FONT.render_to(screen, progress_text_rect, progress_text, "white", size=TEXT_SIZE)

        task_text = f"{self.progress_bar.current_task}"
        task_text_rect = BASIC_FONT.get_rect(task_text, size=TEXT_SIZE)
        task_text_rect.center = (
            screen.get_rect().center[0],
            screen.get_rect().center[1] + progress_text_rect.height + 10,
        )
        BASIC_FONT.render_to(screen, task_text_rect, task_text, "white", size=TEXT_SIZE)
