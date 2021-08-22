from citygame.src.util.locations import calculate_locations
from citygame.src.util.maps import generate_map


class TestLocations:
    def test_calculate_locations(self):
        map_size = 100
        map_object = generate_map(map_size, map_size)

        locations = calculate_locations(map_object)
        assert len(locations) > 0
