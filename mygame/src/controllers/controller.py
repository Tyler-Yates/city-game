import logging
from typing import List

import pygame

from mygame.src.controllers.scene_controller import SceneController
from mygame.src.interfaces.overlay import Overlay
from mygame.src.state.game_state import GameState


class Controller:
    """
    The main controller that orchestrates all the game pieces.
    """

    def __init__(
        self,
        game_name: str,
        game_state: GameState,
        scene_controller: SceneController,
        fps: int,
        width_px: int,
        height_px: int,
        overlays: List[Overlay],
    ):
        self.log = logging.getLogger(self.__class__.__name__)
        self.game_name = game_name
        self.fps = fps
        self.width_px = width_px
        self.height_px = height_px
        self.game_state = game_state
        self.scene_controller = scene_controller
        self.overlays = overlays
        self.clock = pygame.time.Clock()

        self.log.info(f"Starting game with resolution {self.width_px}x{self.height_px} at {self.fps} FPS")

        # Use a boolean to know when to break out of the game loop
        self.quit_flag = False

        # Set up the window
        self.screen = pygame.display.set_mode((self.width_px, self.height_px))
        pygame.display.set_caption(self.game_name)

    def loop(self):
        scene = self.scene_controller.get_active_scene()
        while not self.quit_flag:
            millis_since_last_frame = self.clock.tick(self.fps)
            time_delta = float(millis_since_last_frame) / 1000.0

            # Exit events
            events = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    events.append(event)

            # Input processing
            scene.process_input(events)
            for overlay in self.overlays:
                overlay.process_input(events)

            # Updating
            scene.update(time_delta)
            for overlay in self.overlays:
                overlay.update(time_delta)

            # Rendering
            scene.render(self.screen)
            for overlay in self.overlays:
                overlay.render(self.screen)

            # We do not want to change scenes mid-frame so wait until the end of the frame to change scenes
            scene = self.scene_controller.get_active_scene()

            pygame.display.flip()

    def quit(self):
        self.quit_flag = True
