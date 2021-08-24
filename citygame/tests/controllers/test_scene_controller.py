import pytest as pytest

from citygame.src.constants.scene_enum import SceneEnum
from citygame.src.controllers.scene_controller import SceneController
from citygame.src.interfaces.scene import Scene
from citygame.src.state.game_state import GameState


class TestSceneController:
    @pytest.fixture(scope="function")
    def scene_controller(self):
        game_state: GameState = GameState(map_size=1)
        scene_controller = SceneController(game_state)
        return scene_controller

    def test_get_scene_object(self, scene_controller):
        """Assert that every value in SceneEnum can be created by the scene controller."""

        for value in SceneEnum:
            scene_object = scene_controller._get_scene_object(value)
            assert isinstance(scene_object, Scene)
