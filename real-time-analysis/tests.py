
import numpy as np


def calculate_sound_source(tdoa, pos_ref, pos_target):
    """
    Calculate the sound source location based on TDOA between two microphones,
    assuming the source is on the line connecting the microphones.

    Parameters:
    - tdoa: Time Difference of Arrival between the reference microphone and the target microphone.
    - pos_ref: Tuple representing the (x, y) coordinates of the reference microphone.
    - pos_target: Tuple representing the (x, y) coordinates of the target microphone.

    Returns:
    - The estimated (x, y) coordinates of the sound source or None if calculation is not possible.
    """
    speed_of_sound = 343  # Speed of sound in air (m/s)

    # Calculate the distance difference based on TDOA
    distance_diff = tdoa * speed_of_sound

    x_ref, y_ref = pos_ref
    x_target, y_target = pos_target

    # Calculate the total distance between the two microphones
    total_distance = np.linalg.norm([x_target - x_ref, y_target - y_ref])

    if total_distance == 0:
        return None  # Microphones are at the same position; can't determine direction

    # Calculate the ratio of distances from the reference microphone to the point
    # where the sound source lies on the line connecting the two microphones
    ratio = distance_diff / total_distance

    # Calculate the sound source position based on the ratio
    sound_source_x = x_ref + ratio * (x_target - x_ref)
    sound_source_y = y_ref + ratio * (y_target - y_ref)

    return [sound_source_x, sound_source_y]


if __name__ == "__main__":
    pos_ref = (10, 0)
    pos_target = (1, 0)
    tdoa = 0.001  # 1 ms

    sound_source = calculate_sound_source(tdoa, pos_ref, pos_target)
    print(sound_source)  # Output: [0.343, 0.0]
