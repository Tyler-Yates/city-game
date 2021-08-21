import logging
from random import randrange
from typing import List, TYPE_CHECKING

from pygame import Surface
from pygame.event import Event

from mygame.src.constants.game_constants import MAXIMUM_ASTEROID_SIZE
from mygame.src.constants.scene_enum import SceneEnum
from mygame.src.interfaces.scene import Scene
from mygame.src.state.asteroid_actor import Asteroid
from mygame.src.state.game_state import GameState
from mygame.src.util.fonts import BASIC_FONT, render_with_outline
from mygame.src.util.polygons import collides

if TYPE_CHECKING:
    from mygame.src.controllers.scene_controller import SceneController

BACKGROUND_COLOR = (50, 50, 50)

MINIMUM_ASTEROID_TICK = 100
BASE_MAXIMUM_ASTEROID_TICK = 4000

SCORE_TEXT_PREFIX = "Score: "
SCORE_TEXT_SIZE = 20


class GameScene(Scene):
    """
    Scene that handles actual gameplay.
    """

    def __init__(self, game_state: GameState, scene_controller: "SceneController"):
        super().__init__(game_state, scene_controller)

        self.log = logging.getLogger(self.__class__.__name__)

        self.asteroid_tick = 0
        self.next_asteroid_tick = 5000
        self.maximum_asteroids_on_screen = 5

        # We keep track of score as a float since there may be more than one frame per tenth of a second
        self.score_float = float(game_state.score)

    def process_input(self, events: List[Event]):
        self.game_state.player.process_input(events)

    def update(self, time_delta: float):
        # Move the player
        self.game_state.player.update(time_delta)

        # Check for any collisions and end the game if there are any
        player_collision_polygon = self.game_state.player.get_collision_polygon()
        for asteroid in self.game_state.asteroids:
            asteroid.update(time_delta)
            asteroid_collision_polygon = asteroid.get_collision_polygon()
            if collides(player_collision_polygon, asteroid_collision_polygon):
                self.scene_controller.change_active_scene(SceneEnum.GameOver)

        # Increase score by one every tenth of a second
        self.score_float += time_delta * 10
        self.game_state.score = round(self.score_float)

        # Generate an asteroid if it is time to do so and there are not too many on screen
        if (self.asteroid_tick > self.next_asteroid_tick) and (
            len(self.game_state.asteroids) < self.maximum_asteroids_on_screen
        ):
            self.asteroid_tick = 0
            self._create_asteroid_and_set_next_ticket()

        # Update ticks for time-based events
        tick = int(time_delta * 1000)
        self.asteroid_tick += tick

    def _create_asteroid_and_set_next_ticket(self):
        # Generate a new asteroid
        self.game_state.asteroids.append(Asteroid())

        # Calculate when the next asteroid should be generated
        if self.game_state.score < 300:
            self.next_asteroid_tick = randrange(MINIMUM_ASTEROID_TICK, BASE_MAXIMUM_ASTEROID_TICK)
        elif self.game_state.score < 600:
            self.next_asteroid_tick = randrange(MINIMUM_ASTEROID_TICK, int(BASE_MAXIMUM_ASTEROID_TICK / 2))
        elif self.game_state.score < 1200:
            self.next_asteroid_tick = randrange(MINIMUM_ASTEROID_TICK, int(BASE_MAXIMUM_ASTEROID_TICK / 4))
        else:
            self.next_asteroid_tick = randrange(MINIMUM_ASTEROID_TICK, int(BASE_MAXIMUM_ASTEROID_TICK / 8))

        # Adjust how many asteroids can be on the screen
        if self.game_state.score < 600:
            self.maximum_asteroids_on_screen = 5
        elif self.game_state.score < 1200:
            self.maximum_asteroids_on_screen = 7
        elif self.game_state.score < 1200:
            self.maximum_asteroids_on_screen = 8
        else:
            self.maximum_asteroids_on_screen = 9

        self.log.debug(
            f"Creating new asteroid. Next tick: {self.next_asteroid_tick}. "
            f"Existing asteroids: {len(self.game_state.asteroids)}"
        )

    def render(self, screen: Surface):
        screen.fill(BACKGROUND_COLOR)

        # Player
        self.game_state.player.render(screen)

        # Only keep asteroids that have not gone too far below the screen.
        self.game_state.asteroids[:] = [
            asteroid
            for asteroid in self.game_state.asteroids
            if asteroid.pos_y < screen.get_height() + MAXIMUM_ASTEROID_SIZE * 2
        ]

        # Now render any asteroids left
        for asteroid in self.game_state.asteroids:
            asteroid.render(screen)

        # Score in upper-left
        score_text = SCORE_TEXT_PREFIX + str(self.game_state.score)
        render_with_outline(screen, BASIC_FONT, (5, 5), score_text, SCORE_TEXT_SIZE, "white", BACKGROUND_COLOR)
