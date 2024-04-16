from __future__ import annotations
from math import sqrt, pow, tan, pi


class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def distance(self, point: Point):
        """ Gives the distance between two points. """
        return sqrt(pow(self.x - point.x, 2) +
                    pow(self.y - point.y, 2) +
                    pow(self.z - point.z, 2))


class Scenario:
    SOUND_VELOCITY = 343

    def __init__(self, sender: Point, receivers: tuple[Point, ...],
                 description: str = ""):
        self.sender: Point = sender
        self.receivers: tuple[Point, ...] = receivers
        self.description: str = description

    def distances(self) -> tuple[float, ...]:
        """ Get the all receivers distances to the sender. """
        return tuple(point.distance(self.sender) for point in self.receivers)

    def relative_distances(self) -> tuple[float, ...]:
        """
        Get receivers distances to the sender relative to the eachother.
        """
        distances: tuple[float, ...] = self.distances()
        min_distance: float = min(distances)
        return tuple(distance - min_distance for distance in distances)

    def relative_time_arrivals(self) -> tuple[float, ...]:
        """
        Get receivers relative time offset when receiving a sound signal
        from the sender
        """
        relative_distances = self.relative_distances()
        return tuple(relative_distance / self.SOUND_VELOCITY for
                     relative_distance in relative_distances)


# Helper functions

def equilateral_triangle_top(point: Point) -> Point:
    """
    Get the top coordinate of a equilateral triangle relative to the side
    length of the triangle. The parameter point decides the length and
    orientation of the triangle.

    *Assuming one point of the triangle is on origo and one is on one of
    the axes
    """
    half_side_length: float = point.distance(Point()) / 2
    if point.x != 0:
        return Point(half_side_length, half_side_length * tan(pi / 3))
    else:
        return Point(half_side_length * tan(pi / 3), half_side_length)


def equilateral_triangle_center(point: Point) -> Point:
    """
    Get the middle coordinate of a equilateral triangle. The parameter
    point decides the length and orientation of the triangle.
    triangle.

    *Assuming one point of the triangle is on origo and one is on one of
    the axes
    """
    half_side_length: float = point.distance(Point()) / 2
    if point.x != 0:
        return Point(half_side_length, half_side_length * tan(pi / 6))
    else:
        return Point(half_side_length * tan(pi / 6), half_side_length)
