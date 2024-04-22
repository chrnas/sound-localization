from __future__ import annotations
from math import sqrt, pow, tan, pi


class Point:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x: float = float(x)
        self.y: float = float(y)
        self.z: float = float(z)

    def distance(self, point: Point):
        """ Gives the distance between two points. """
        x_diff = self.x - point.x
        y_diff = self.y - point.y
        z_diff = self.z - point.z
        return sqrt(pow(x_diff, 2) + pow(y_diff, 2) + pow(z_diff, 2))

    def __repr__(self):
        return f"({round(self.x, 1)}, {round(self.y, 1)}, {round(self.z, 1)})"


class Scenario:
    SOUND_VELOCITY = 343

    def __init__(self, sender: Point, receivers: tuple[Point, ...],
                 description: str = ""):
        self.sender: Point = sender
        self.receivers: tuple[Point, ...] = receivers
        self.description: str = description

    def distances(self) -> tuple[float, ...]:
        """ Get the distances from all receivers to the sender. """
        return tuple(point.distance(self.sender) for point in self.receivers)

    def relative_distances(self) -> tuple[float, ...]:
        """
        Get receivers distances to the sender relative to each other.
        """
        distances: tuple[float, ...] = self.distances()
        min_distance: float = min(distances)
        return tuple(round(distance - min_distance, 10) for
                     distance in distances)

    def relative_time_arrivals(self) -> tuple[float, ...]:
        """
        Get receivers relative time offset when receiving a sound signal
        from the sender.
        """
        relative_distances = self.relative_distances()
        return tuple(round(relative_distance / self.SOUND_VELOCITY, 10) for
                     relative_distance in relative_distances)

    def __repr__(self):
        sender_receivers = "".join((
            str(receiver).ljust(25, " ")
            for receiver in (self.sender,) + self.receivers))
        return sender_receivers + f"{self.description}"


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


def print_header(receivers: tuple[Point, ...]):
    columns = ["Sender"] + [receiver for receiver in receivers] + \
        ["Description"]
    head = "".join((str(column).ljust(25, " ") for column in columns))
    print(head)


def print_scenarios(receivers: tuple[Point, ...],
                    scenarios: tuple[Scenario, ...]
                    ):
    print_header(receivers)
    for scenario in scenarios:
        print(scenario)


def print_relative_arrivals(receivers: tuple[Point, ...],
                            scenarios: tuple[Scenario, ...]):
    print_header(receivers)
    for scenario in scenarios:
        row = (scenario.sender,) + scenario.relative_time_arrivals()
        relative_arrivals = "".join((
            str(receiver).ljust(25, " ")
            for receiver in row))
        print(relative_arrivals + f"{scenario.description}")
