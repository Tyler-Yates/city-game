import pytest

from mygame.src.util.polygons import collides, generate_polygon


class TestCollisions:
    def test_collides_true(self):
        base_polygon = [[0, 0], [2, 2], [4, 0]]

        # A polygon should always collide with itself
        assert collides(base_polygon, base_polygon)

        # This polygon is contained completely within base_polygon
        contained_within_polygon = [[0, 0], [1, 1], [2, 0]]
        assert collides(base_polygon, contained_within_polygon)

        # This polygon touches base_polygon only at (0, 0) but that is still a collision
        one_pixel_collision_polygon = [[0, 0], [-2, -2], [-4, 0]]
        assert collides(base_polygon, one_pixel_collision_polygon)

    def test_collides_false(self):
        polygon1 = [[0, 0], [2, 2], [4, 0]]

        # No collision
        not_collides_polygon1 = [[-1, 0], [-2, -2], [-4, 0]]
        assert not collides(polygon1, not_collides_polygon1)

    def test_generate_polygon_invalid(self):
        # Must have at least 3 vertices
        with pytest.raises(ValueError):
            self._test_generate_polygon(-1, 10, 0)
            self._test_generate_polygon(0, 10, 0)
            self._test_generate_polygon(1, 10, 0)
            self._test_generate_polygon(2, 10, 0)

        # Size must be at least 2
        with pytest.raises(ValueError):
            self._test_generate_polygon(3, -1, 0)
            self._test_generate_polygon(3, 0, 0)
            self._test_generate_polygon(3, 1, 0)

    def test_generate_polygon_valid(self):
        self._test_generate_polygon(3, 2, 0)
        self._test_generate_polygon(3, 10, 0)
        self._test_generate_polygon(100, 100, 1.0)
        self._test_generate_polygon(100, 100, 2.0)

    @staticmethod
    def _test_generate_polygon(num_vertices: int, size: int, variance: float):
        polygon = generate_polygon(num_vertices, size, variance)
        assert len(polygon) == num_vertices
