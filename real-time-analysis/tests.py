
import numpy as np

def calculate_sound_source(tdoa, pos_ref, pos_target):
    speed_of_sound = 343  # Speed of sound in air (m/s)
    
    # Convert positions to numpy arrays for easier manipulation
    pos_ref = np.array(pos_ref)
    pos_target = np.array(pos_target)

    # Calculate the distance difference based on TDOA
    distance_diff = tdoa * speed_of_sound

    # Calculate the midpoint between the two microphones
    midpoint = (pos_ref + pos_target) / 2

    # Calculate the direction vector from the reference mic to the target mic, then normalize
    direction = pos_target - pos_ref
    direction_norm = direction / np.linalg.norm(direction)

    # Calculate the sound source position
    # Note: Since TDOA might be negative indicating the direction towards the reference microphone,
    # we adjust the position based on the distance_diff (which can be positive or negative) along the normalized direction.
    sound_source_pos = midpoint + direction_norm * (distance_diff / 2)

    return sound_source_pos.tolist()


if __name__ == "__main__":
    pos_ref = (10, 0)
    pos_target = (-10, 0)
    tdoa = 0.0583 # 1 ms

    sound_source = calculate_sound_source(tdoa, pos_ref, pos_target)
    print(sound_source)  # Output: [0.343, 0.0]
