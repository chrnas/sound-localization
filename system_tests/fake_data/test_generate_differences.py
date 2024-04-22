import pytest
from math import sqrt, tan, pi
from scenarios import (
    SCENARIOS_15M,
    SCENARIOS_25M,
    SCENARIOS_35M,
    SCENARIOS_3D,
)
from generate_differences import (
    Point,
    Scenario,
)


@pytest.mark.parametrize(["args", "expected"], [
    ((Point(), Point(1, 1, 1)), sqrt(3)),
    ((Point(1, 0, 0), Point(1, 2, 0)), 2),
    ((Point(1, 1, 3), Point(2, 2, 3)), sqrt(2))
])
def test_distance(args, expected):
    point1: Point = args[0]
    point2: Point = args[1]
    assert round(point1.distance(point2), 10) == round(expected, 10)


@pytest.mark.parametrize(["args", "expected"], [
    ((SCENARIOS_15M[3],),
     (0, 0, 0)),
    ((SCENARIOS_35M[4],),
     (0,
      round(sqrt(10**2 + 35**2) - 10, 10),
      round(sqrt((17.5 * tan(pi / 3) - 10)**2 + 17.5**2) - 10, 10))),
    ((SCENARIOS_3D[0],),
     (0,
      round(sqrt(2 * 15**2 + 5.3**2) - sqrt(2*15**2), 10), 0,
      round(sqrt(2 * 15**2 + 5.3**2) - sqrt(2 * 15**2), 10)))
])
def test_relative_distances(args, expected):
    scenario: Scenario = args[0]
    assert scenario.relative_distances() == expected, f"{scenario.sender}, {
        scenario.receivers}"


@pytest.mark.parametrize(["args", "expected"], [
    ((SCENARIOS_25M[1],),
     (round(25 / 343, 10), 0, round(25 / 343, 10))),
    ((SCENARIOS_3D[0],),
     (0,
      round((sqrt(2 * 15**2+5.3**2) - sqrt(2*15**2)) / 343, 10),
      0,
      round((sqrt(2 * 15**2 + 5.3**2) - sqrt(2 * 15**2)) / 343, 10)))
])
def test_relative_arrivals(args, expected):
    scenario: Scenario = args[0]
    assert scenario.relative_time_arrivals() == expected
