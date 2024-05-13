from .gridtrilaterate import get_distance, GridTravelSettings, trilaterate_grid
from .receiver import Receiver
import time
import pytest
import numpy as np

# Constants for the test
STEP = 0.5  # Step size for the grid [m]
EXPANSION = 5  # Expansion factor for the search grid [m]
TIME_LIMIT = 1.5  # Maximum allowable time for the test to run [s]
ACCURACY = 0.5  # Maximum allowable error [m]


test_cases = [
    ([[0, 0], [0, 15], [13, 7.5]], [0, 0]),
    ([[0, 0], [0, 15], [13, 7.5]], [0, 15]),
    ([[0, 0], [0, 15], [13, 7.5]], [13, 7.5]),
    ([[0, 0], [0, 15], [13, 7.5]], [4.5, 7.5]),
    ([[0, 0], [0, 15], [13, 7.5]], [10, 0]),
    ([[0, 0], [0, 15], [13, 7.5]], [0, 7.5]),
    ([[0, 0], [0, 15], [13, 7.5]], [5, 5]),
    ([[0, 0], [0, 15], [13, 7.5]], [3, 10]),

    ([[0, 0], [0, 25], [21.5, 12.5]], [0, 0]),
    ([[0, 0], [0, 25], [21.5, 12.5]], [0, 25]),
    ([[0, 0], [0, 25], [21.5, 12.5]], [21.5, 12.5]),
    ([[0, 0], [0, 25], [21.5, 12.5]], [7, 12.5]),
    ([[0, 0], [0, 25], [21.5, 12.5]], [10, 0]),
    ([[0, 0], [0, 25], [21.5, 12.5]], [0, 10]),
    ([[0, 0], [0, 25], [21.5, 12.5]], [4, 11]),
    ([[0, 0], [0, 25], [21.5, 12.5]], [13, 13]),

    ([[0, 0], [0, 35], [30.5, 17.5]], [0, 0]),
    ([[0, 0], [0, 35], [30.5, 17.5]], [0, 35]),
    ([[0, 0], [0, 35], [30.5, 17.5]], [30.5, 17.5]),
    ([[0, 0], [0, 35], [30.5, 17.5]], [10, 17.5]),
    ([[0, 0], [0, 35], [30.5, 17.5]], [10, 0]),
    ([[0, 0], [0, 35], [30.5, 17.5]], [0, 10]),
    ([[0, 0], [0, 35], [30.5, 17.5]], [17.5, 17.5]),
    ([[0, 0], [0, 35], [30.5, 17.5]], [3, 27]),

    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]], [15, 15, 0]),
    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]], [15, 15, 2.5]),
    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]], [10, 0, 0]),
    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]], [10, 0, 2.5]),
    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]], [0, 30, 0]),
    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]], [0, 30, 2.5]),
    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]], [25, 20, 0]),
    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]], [25, 20, 2.5]),
    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]], [5, 20, 0]),
    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]], [5, 20, 2.5]),
    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]], [35, 35, 0]),
    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]], [35, 35, 2.5]),

    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5], [15, 15, 0]], [35, 35, 2.5]),
    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5], [15, 15, 0]], [-1, -1, 0]),
    ([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5], [15, 15, 0]], [15, 15, 0])
]


# Utility function to create receivers with adjusted distances
def create_mics(actual_pos, mic_positions):
    distances = [get_distance(actual_pos, mic) for mic in mic_positions]
    first_dist = distances[0]
    distances = [dist - first_dist for dist in distances]
    mics = [Receiver(pos) for pos in mic_positions]
    for i, mic in enumerate(mics):
        mic.set_distance_difference(distances[i])
    return mics


@pytest.mark.parametrize("mic_positions, actual_pos", test_cases)
def test_positioning_accuracy(mic_positions, actual_pos):
    settings = GridTravelSettings(len(mic_positions[0]), STEP)
    settings.smallest_expansion = [EXPANSION] * \
        len(settings.smallest_expansion)
    settings.biggest_expansion = [EXPANSION] * len(settings.smallest_expansion)

    start_time = time.time()
    mics = create_mics(actual_pos, mic_positions)
    result_pos = trilaterate_grid(mics, settings)
    assert np.linalg.norm(np.array(result_pos) - np.array(actual_pos)
                          ) <= ACCURACY, f"Position {actual_pos} not within accuracy limits, it had an error of {np.linalg.norm(np.array(result_pos) - np.array(actual_pos))}"
    assert time.time() - \
        start_time < TIME_LIMIT, f"Calculation exceeded time limit for position {
            actual_pos}"
