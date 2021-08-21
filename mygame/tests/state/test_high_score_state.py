import os

import pytest

from mygame.src.state.high_score_state import HighScoreState
from mygame.src.util.paths import get_save_file_directory

TEST_SAVE_FILE_NAME = "test_save.json"


class TestHighScoreState:
    @staticmethod
    def _create_high_score_state() -> HighScoreState:
        return HighScoreState(save_file_name=TEST_SAVE_FILE_NAME)

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        # Code that will run before each test case
        save_file_path = os.path.join(get_save_file_directory(), TEST_SAVE_FILE_NAME)
        if os.path.exists(save_file_path):
            os.remove(save_file_path)

        # A test function will be run at this point
        yield

        # Code that will run after your test, for example:
        pass

    def test_save_high_scores(self):
        # Add some scores to the HighScoreState and then save
        high_score_state_1 = self._create_high_score_state()
        high_scores = [300, 200, 100]
        for score in high_scores:
            high_score_state_1.add_high_score(score)
        high_score_state_1.save_high_scores()

        # Create a new instance of HighScoreState to simulate restarting the game.
        # The existing scores should persist to this new HighScoreState.
        high_score_state_2 = self._create_high_score_state()
        assert high_scores == high_score_state_2.get_high_scores()
