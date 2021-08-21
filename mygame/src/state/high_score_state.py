import json
import logging
import os
from pathlib import Path
from typing import List

from mygame.src.util.paths import get_save_file_directory

MAXIMUM_NUMBER_OF_HIGH_SCORES = 10

HIGH_SCORE_KEY = "high_scores"

DEFAULT_SAVE_FILE_NAME = "save.json"


class HighScoreState:
    def __init__(self, save_file_name: str = None):
        self.log = logging.getLogger(self.__class__.__name__)
        self.high_scores: List[int] = []

        self.save_file_name = DEFAULT_SAVE_FILE_NAME if save_file_name is None else save_file_name
        self.save_file_path = os.path.join(get_save_file_directory(), self.save_file_name)

        # Attempt to load the save file from disk
        self.high_scores = self._load_save_file()
        self._cleanup_high_scores()

    def _cleanup_high_scores(self):
        self.high_scores = sorted(self.high_scores, reverse=True)
        self.high_scores = self.high_scores[:MAXIMUM_NUMBER_OF_HIGH_SCORES]

    def _load_save_file(self) -> List[int]:
        if not os.path.exists(self.save_file_path):
            self.log.info(f"No save file found at {self.save_file_path}")
            return []

        try:
            with open(self.save_file_path, mode="r") as save_file:
                json_data = json.load(save_file)
                return json_data[HIGH_SCORE_KEY]
        except Exception as e:
            self.log.error("Could not load high score file.", e)
            return []

    def get_high_scores(self) -> List[int]:
        """
        Returns the high scores in order from largest to smallest.

        Returns:
            The high scores in sorted order
        """
        return self.high_scores

    def add_high_score(self, score: int) -> bool:
        """
        Attempts to add the given score the high score table.
        Returns whether the score is good enough to make it onto the high score table.

        Args:
            score: The given score

        Returns:
            True if the score is good enough to make it on the high score table, False otherwise
        """
        if len(self.high_scores) < MAXIMUM_NUMBER_OF_HIGH_SCORES or (score > self.high_scores[-1]):
            self.high_scores.append(score)
            self._cleanup_high_scores()
            return True
        else:
            return False

    def save_high_scores(self):
        self.log.info(f"Saving high scores to {self.save_file_path}")

        Path(get_save_file_directory()).mkdir(parents=True, exist_ok=True)

        with open(self.save_file_path, mode="w") as save_file:
            data_to_save = {HIGH_SCORE_KEY: self.high_scores}
            json.dump(data_to_save, save_file)
