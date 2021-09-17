import math


def get_level(xp: int) -> int:
    return int(math.sqrt(xp // 100)) + 1


def get_xp_for_location_victory(location_level: int) -> int:
    return location_level * 100
