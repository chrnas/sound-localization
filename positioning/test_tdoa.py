from .calcfunctions import constants
from .calcfunctions.receiver import Receiver
from .methodclass import MethodBaseClass
from .tdoa import MethodClass
from .calcfunctions.receiver import Receiver
import numpy as np


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


def test_method_class():
    positions = [[0, 0], [1, 0], [0, 1], [1, 1]]  # Example positions
    mics = Receiver.create_mics(positions)

    # Assuming the microphone at position [0, 0] detected sound first
    source_pos = [0.5, 0.5]
    setup_time_differences(mics, 0, source_pos)

    method = MethodClass()
    method.set_setting(setting='algorithm', value='grid')
    result = method.find_source(mics)
    print("grid result:", result)
    assert np.linalg.norm(np.array(result) - np.array(source_pos)) <= 2
    method.set_setting(setting='algorithm', value='gradient')
    result = method.find_source(mics)
    print("gradient result:", result)
    assert np.linalg.norm(np.array(result) - np.array(source_pos)) <= 2


# Example constants definition
# Speed of sound in m/s (approximate in air at 20°C)
constants.SOUNDSPEED = 343
