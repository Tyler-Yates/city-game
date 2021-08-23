from typing import List

from citygame.src.state.location_actor import LocationActor
from citygame.src.util.locations import calculate_locations
from citygame.src.util.maps import generate_map


class WorldState:
    """
    Representation of a world.
    """

    def __init__(self, map_size: int = 1024):
        self.map_tiles = generate_map(map_size, map_size)

        location_points = calculate_locations(self.map_tiles)

        self.locations = []
        for location_point in location_points:
            self.locations.append(LocationActor(location_point[0], location_point[1]))

    def get_locations(self) -> List[LocationActor]:
        return self.locations
