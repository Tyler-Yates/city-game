from enum import Enum, auto

from pygame import Color


class LocationState(Enum):
    """
    Enum cataloging the states a location can be in.
    """

    HIDDEN = auto()
    DISCOVERED = auto()
    EXPLORED = auto()
    CONQUERED = auto()

    @staticmethod
    def get_rgb_color(location_state: 'LocationState') -> Color:
        if location_state == LocationState.HIDDEN:
            return Color("black")
        if location_state == LocationState.DISCOVERED:
            return Color("red")
        if location_state == LocationState.EXPLORED:
            return Color(43, 123, 227)
        if location_state == LocationState.CONQUERED:
            return Color("green")

        return Color("black")
