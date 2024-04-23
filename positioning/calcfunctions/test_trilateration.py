from .trilateration import MicrophoneArray
import numpy as np
from typing import Union
import time


TIME_LIMIT = 1.5  # Acceptable time for the function to run [s]
# Acceptable difference between actual and calculated position [m]
ACCURACY = 1


def assert_function(actual_positions: Union[list, np.ndarray], microphone_array: MicrophoneArray) -> None:

    actual_positions = np.array(actual_positions)
    for actual_position in actual_positions:
        start_time: float = time.time()
        actual_position: np.ndarray = np.array(actual_position)
        microphone_array.calculate_time_diffs(actual_position)
        result_position, _ = microphone_array.estimate_position()

        assert np.linalg.norm(actual_position - result_position) <= ACCURACY
        assert time.time() - start_time < TIME_LIMIT


def test_1_8():
    """
    Testing cases 1-8 from "Datainsamlingsplan 4/4". Coordinates are round to closest 0.5.
    """
    mic_positions = [[0, 0], [0, 15], [13, 7.5]]
    microphone_array: MicrophoneArray = MicrophoneArray(mic_positions)
    actual_positions = [[0, 0], [0, 15], [13, 7.5], [
        4.5, 7.5], [10, 0], [0, 7.5], [5, 5], [3, 10]]

    assert_function(actual_positions=actual_positions,
                    microphone_array=microphone_array)


def test_9_16():
    """
    Testing cases 9-16 from "Datainsamlingsplan 4/4". Coordinates are round to closest 0.5.
    """
    mic_positions = [[0, 0], [0, 25], [21.5, 12.5]]
    microphone_array: MicrophoneArray = MicrophoneArray(mic_positions)
    actual_positions = [[0, 0], [0, 25], [21.5, 12.5],
                        [7, 12.5], [10, 0], [0, 10], [4, 11], [13, 13]]

    assert_function(actual_positions=actual_positions,
                    microphone_array=microphone_array)


def test_17_24():
    """
    Testing cases 9-16 from "Datainsamlingsplan 4/4". Coordinates are round to closest 0.5.
    """
    mic_positions = [[0, 0], [0, 35], [30.5, 17.5]]
    microphone_array: MicrophoneArray = MicrophoneArray(mic_positions)
    actual_positions = [
        [0, 0],
        [0, 35],
        [30.5, 17.5],
        [10, 17.5],
        [10, 0],
        [0, 10],
        [17.5, 17.5],
        [3, 27]
    ]

    assert_function(actual_positions=actual_positions,
                    microphone_array=microphone_array)


def test_25_36():
    """
    Testing cases 25-36 from "Datainsamlingsplan 4/4". Coordinates are round to closest 0.5.
    """
    mic_positions = [[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]]
    microphone_array: MicrophoneArray = MicrophoneArray(mic_positions)

    actual_positions = [
        [15, 15, 0],
        [15, 15, 2.5],
        [10, 0, 0],
        [10, 0, 2.5],
        [0, 30, 0],
        [0, 30, 2.5],
        [25, 20, 0],
        [25, 20, 2.5],
        [5, 20, 0],
        [5, 20, 2.5],
        [35, 35, 0],
        [35, 35, 2.5]
    ]

    assert_function(actual_positions=actual_positions,
                    microphone_array=microphone_array)


def test_5_microphones():
    """
    Testing some cases with 5 microphones.
    """
    mic_positions = [[0, 0, 0], [0, 30, 5.5], [
        30, 30, 0], [30, 0, 5.5], [15, 15, 0]]
    microphone_array: MicrophoneArray = MicrophoneArray(mic_positions)

    actual_positions = [
        [35, 35, 2.5],
        [-1, -1, 0],
        [15, 15, 0]
    ]

    assert_function(actual_positions=actual_positions,
                    microphone_array=microphone_array)
