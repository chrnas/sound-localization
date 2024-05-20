from .trilateration import MicrophoneArray
import numpy as np
import time
import pytest


TIME_LIMIT = 1.5  # Acceptable time for the function to run [s]
# Acceptable difference between actual and calculated position [m]
ACCURACY = 1


# Collect all test cases with detailed configurations and actual positions.
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

# test_cases = [([[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]], [35, 35, 0])]


@pytest.mark.slow
@pytest.mark.parametrize("mic_positions, actual_position", test_cases)
def test_positioning_accuracy(mic_positions, actual_position):
    """
    Test the accuracy of the positioning method under various scenarios.
    """
    microphone_array = MicrophoneArray(mic_positions)
    start_time = time.time()
    microphone_array.calculate_time_diffs(actual_position)
    # [print(microphone.get_time_difference()) for microphone in microphone_array.get_microphones()]
    result_position, _ = microphone_array.estimate_position()
    # microphone_array.plot_cost_function(actual_pos=actual_position, estimated_pos=result_position)

    assert np.linalg.norm(np.array(actual_position) - np.array(result_position)
                          ) <= ACCURACY, f"Position {actual_position} not within accuracy limits"
    assert time.time() - \
        start_time < TIME_LIMIT, f"Calculation exceeded time limit for position {
            actual_position}"
