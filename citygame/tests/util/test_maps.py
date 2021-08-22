import numpy

from citygame.src.util.maps import generate_map


class TestMaps:
    def test_generate_map(self):
        map_size = 100
        map_object = generate_map(map_size, map_size)

        assert not numpy.isnan(map_object).any()
        assert not numpy.isinf(map_object).any()
