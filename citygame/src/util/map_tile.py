from enum import Enum, auto
from typing import List


class MapTile(Enum):
    DEEP_WATER = auto()
    SHALLOW_WATER = auto()
    BEACH = auto()
    GRASSLAND = auto()
    FOREST = auto()
    MOUNTAIN = auto()
    SNOW = auto()

    @staticmethod
    def get_rgb_value(tile) -> List[int]:
        tile = int(tile)

        if tile == MapTile.DEEP_WATER.value:
            return [0, 62, 173]
        elif tile == MapTile.SHALLOW_WATER.value:
            return [9, 82, 200]
        elif tile == MapTile.BEACH.value:
            return [238, 214, 175]
        elif tile == MapTile.GRASSLAND.value:
            return [34, 139, 34]
        elif tile == MapTile.FOREST.value:
            return [0, 100, 0]
        elif tile == MapTile.MOUNTAIN.value:
            return [139, 137, 137]
        elif tile == MapTile.SNOW.value:
            return [255, 250, 250]
