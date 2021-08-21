from typing import List, TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.event import Event

from mygame.src.constants.scene_enum import SceneEnum
from mygame.src.interfaces.scene import Scene
from mygame.src.state.game_state import GameState
from mygame.src.util.fonts import BASIC_FONT, MONOSPACE_FONT

if TYPE_CHECKING:
    from mygame.src.controllers.scene_controller import SceneController

BACKGROUND_COLOR = (0, 0, 0)

GAME_OVER_TEXT = "Game Over"
MAIN_MENU_TEXT_SIZE = 64
SCORE_TEXT_SIZE = 32
CONTINUE_TEXT_SIZE = 24


class GameOverScene(Scene):
    """
    GameOverScene
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController"):
        super().__init__(game_state, scene_controller)

        # Add score to the high score table and save to disk
        self.is_new_high_score = self.game_state.high_scores.add_high_score(self.game_state.score)
        self.game_state.high_scores.save_high_scores()

    def process_input(self, events: List[Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Pressing Return will take you to the game
                if event.key == pygame.K_RETURN:
                    # Reset the game state since the game is over
                    self.game_state.reset()
                    self.scene_controller.change_active_scene(SceneEnum.MainMenu)

    def update(self, time_delta: float):
        pass

    def render(self, screen: Surface):
        screen.fill(BACKGROUND_COLOR)

        screen_center = screen.get_rect().center
        left_center = (screen_center[0] / 2, screen_center[1])
        right_center = (screen_center[0] * 3 / 2, screen_center[1])

        # Game over text
        game_over_rect = BASIC_FONT.get_rect(GAME_OVER_TEXT, size=MAIN_MENU_TEXT_SIZE)
        game_over_rect.center = (screen_center[0], 100)
        BASIC_FONT.render_to(screen, game_over_rect, GAME_OVER_TEXT, "white", size=MAIN_MENU_TEXT_SIZE)

        # Press Enter to continue
        continue_text = "Press Enter to go back to Main Menu"
        continue_text_rect = BASIC_FONT.get_rect(continue_text, size=CONTINUE_TEXT_SIZE)
        continue_text_rect.center = (game_over_rect.center[0], game_over_rect.center[1] + 50)
        BASIC_FONT.render_to(screen, continue_text_rect, continue_text, "white", size=CONTINUE_TEXT_SIZE)

        # Score text
        score_text = f"Your score: {self.game_state.score}"
        score_text_rect = BASIC_FONT.get_rect(score_text, size=SCORE_TEXT_SIZE)
        score_text_rect.center = (left_center[0], left_center[1] - 100)
        BASIC_FONT.render_to(screen, score_text_rect, score_text, "white", size=SCORE_TEXT_SIZE)

        # New High Score text
        if self.is_new_high_score:
            new_high_score_text = "New High Score!"
            new_high_score_text_rect = BASIC_FONT.get_rect(new_high_score_text, size=SCORE_TEXT_SIZE)
            new_high_score_text_rect.center = (score_text_rect.center[0], score_text_rect.center[1] + 50)
            BASIC_FONT.render_to(screen, new_high_score_text_rect, new_high_score_text, "yellow", size=SCORE_TEXT_SIZE)

        # High Score Title
        high_score_title_text = "High Scores"
        high_score_title_text_rect = BASIC_FONT.get_rect(high_score_title_text, size=SCORE_TEXT_SIZE)
        high_score_title_text_rect.center = (right_center[0], right_center[1] - 100)
        BASIC_FONT.render_to(screen, high_score_title_text_rect, high_score_title_text, "white", size=SCORE_TEXT_SIZE)

        # High Scores
        offset = 0
        vertical_spacing = MONOSPACE_FONT.get_rect("9", size=SCORE_TEXT_SIZE).height + 5
        for score in self.game_state.high_scores.high_scores:
            high_score_text = str(score)
            high_score_text_rect = MONOSPACE_FONT.get_rect(high_score_text, size=SCORE_TEXT_SIZE)
            high_score_text_rect.midright = (
                screen.get_rect().right - 100,
                high_score_title_text_rect.bottom + 25 + offset * vertical_spacing,
            )
            MONOSPACE_FONT.render_to(screen, high_score_text_rect, high_score_text, "white", size=SCORE_TEXT_SIZE)
            offset += 1
