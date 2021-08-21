import logging
import os.path
import pathlib
import sys

from mygame.src.constants.game_constants import SAVE_FOLDER_NAME

LOG = logging.getLogger("PathsUtil")


def get_save_file_directory() -> str:
    home_directory = str(pathlib.Path.home().absolute())

    # Default to relative path
    save_file_directory = os.path.join(os.getcwd(), "saves")

    if sys.platform.startswith("win32"):
        save_file_directory = os.path.join(home_directory, f"AppData/Local/Saved Games/{SAVE_FOLDER_NAME}")
    elif sys.platform.startswith("linux"):
        save_file_directory = os.path.join(home_directory, f"saves/{SAVE_FOLDER_NAME}")
    elif sys.platform.startswith("darwin"):
        save_file_directory = os.path.join(home_directory, f"Documents/SavedGames/{SAVE_FOLDER_NAME}")
    else:
        LOG.warning("Could not determine OS!")

    return save_file_directory
