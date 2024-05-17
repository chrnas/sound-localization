from .calcfunctions import constants
from .calcfunctions.receiver import Receiver
from .tdoa import TDOAMethod, calculate_time_differences, MethodClass
import numpy as np
from .TidsförskjutningBeräkning import calc_offset_from_samples


def setup_time_differences(mics, first_detected_index, source_pos):
    """ Setup time differences, assuming the first detected index has a time difference of zero."""
    # Assuming the first_detected_index microphone heard the sound first
    sound_speed = constants.SOUNDSPEED  # Speed of sound constant
    first_mic = mics[first_detected_index]

    # Set time difference for the first detected microphone
    first_mic.set_time_difference(0)

    def generate_pairs_with_first(microphone_list: list[Receiver]) -> list[tuple[Receiver, Receiver]]:

        first_mic = microphone_list[0]
        return [(first_mic, mic) for mic in microphone_list[1:]]

    source_pos = np.array(
        source_pos)  # Ensure source position is an ndarray.
    pairs = generate_pairs_with_first(mics)
    # Time difference for the first microphone is always zero.
    mics[0].set_time_difference(0.0)
    for first_mic, mic in pairs:
        distance = np.linalg.norm(source_pos - mic.get_position())
        reference_distance = np.linalg.norm(
            source_pos - first_mic.get_position())
        time_diff = (distance - reference_distance) / sound_speed
        mic.set_time_difference(time_diff)

    # Sort mics by their time differences
    mics.sort(key=lambda x: x.distance_difference)

# Example test setup


def test_calculate_time_differences():
    # Mock Receivers with associated sound samples
    receiver1 = Receiver([10, 10])
    receiver2 = Receiver([20, 20])
    receiver3 = Receiver([30, 30])

    # Mock sound data where the "detection" times are defined by index of '1'
    receivers = {
        receiver1: [0, 0, 0, 1, 0],  # Detected later
        receiver2: [0, 1, 0, 0, 0],  # Detected first
        receiver3: [0, 0, 1, 0, 0],  # Detected second
    }

    calculate_time_differences(receivers)

    # Validate that time differences are set correctly
    # Expected time differences based on mock sound data positions
    assert receiver1.get_time_difference(
    ) == 2, "Time difference for Receiver 1 is incorrect"
    assert receiver2.get_time_difference(
    ) == 0, "Time difference for Receiver 2 is incorrect"
    assert receiver3.get_time_difference(
    ) == 1, "Time difference for Receiver 3 is incorrect"


def test_method_class():
    # Mock Receivers with associated sound sample lists
    receiver1 = Receiver([0, 1])
    receiver2 = Receiver([1, 0])
    receiver3 = Receiver([-1, 0])

    # Mock sound data where the "detection" times are defined by index of '1'
    mic_data = {
        receiver1: [0, 0, 1, 0, 0],  # Detected later
        receiver2: [0, 0, 1, 0, 0],  # Detected first
        receiver3: [0, 0, 1, 0, 0]   # Detected second
    }

    # Create MethodClass instance
    method = TDOAMethod()

    source_position: np.ndarray = np.array([0, 0])

    # Test with "grid" algorithm
    method.set_setting('algorithm', 'grid')
    result = method.find_source(mic_data)

    assert np.linalg.norm(np.array(
        result) - source_position) <= 0.5, "Grid algorithm failed to locate source accurately"

    # Test with "gradient" algorithm
    method.set_setting('algorithm', 'gradient')
    result = method.find_source(mic_data)

    assert np.linalg.norm(np.array(
        result) - source_position) <= 0.5, "Gradient algorithm failed to locate source accurately"


def test_identify_first_sound():
    # Create several test cases with the "start" of the sound at different positions
    sounds = [
        [0, 0, 0, 1, 0],  # Detected later
        [0, 0, 0, 0, 1],  # Detected even later
        [0, 1, 0, 0, 0],  # First sound detected here
        [0, 0, 1, 0, 0]   # Detected in the middle
    ]

    # Run the function
    first_index = identify_first_sound(sounds)

    # Check if the correct index is identified
    assert first_index == 2, "The identify_first_sound function failed to identify the earliest sound correctly."


def identify_first_sound(sounds):
    """
    Identify the first sound file based on cross-correlation time differences.
    The one with the largest negative time difference when compared to others is the first.

    Args:
        sounds (list of list of float): A list where each item is a sound sample list.

    Returns:
        int: Index of the first sound sample list detected.
    """
    min_time_difference = float('inf')
    first_index = 0

    # Choose one sound as a reference, compare it against all others
    reference_sound = sounds[0]

    for i in range(1, len(sounds)):
        time_difference = calc_offset_from_samples(
            sounds[i], reference_sound, rate1=1, rate2=1)

        # If this sound starts before the current reference
        if time_difference < min_time_difference:
            min_time_difference = time_difference
            first_index = i

    # Adjust for the fact that the first sound might not be the reference
    if min_time_difference > 0:
        first_index = 0

    return first_index


# Example constants definition
# Speed of sound in m/s (approximate in air at 20°C)
constants.SOUNDSPEED = 343
