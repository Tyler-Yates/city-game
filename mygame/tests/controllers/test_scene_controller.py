import pytest as pytest

from mygame.src.constants.scene_enum import SceneEnum
from mygame.src.controllers.scene_controller import SceneController
from mygame.src.interfaces.scene import Scene
from mygame.src.state.game_state import GameState


class TestSceneController:
    @pytest.fixture(scope="function")
    def scene_controller(self):
        game_state: GameState = GameState()
        scene_controller = SceneController(game_state)
        return scene_controller

    def test_get_scene_object(self, scene_controller):
        """Assert that every value in SceneEnum can be created by the scene controller."""

        for value in SceneEnum:
            scene_object = scene_controller._get_scene_object(value)
            assert isinstance(scene_object, Scene)
