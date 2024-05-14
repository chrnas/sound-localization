import numpy as np
import time
from scipy.optimize import least_squares


class Microphone:
    def __init__(self, distance, coords):
        self.distance = distance  # Relative distance from the first microphone
        self.coords = np.array(coords)


def residuals(x, mics):
    return [np.linalg.norm(x - mic.coords) - mic.distance for mic in mics]


def find_sound_source(mics, initial_guess):
    result = least_squares(residuals, initial_guess, args=(mics,))
    return result.x


if __name__ == "__main__":
    mic_positions = [
        [10.0, 2.0, 0],  # Coordinates of microphone 1
        [3.0, -25.0, 15],  # Coordinates of microphone 2
        [25.0, 6.0, 10],  # Coordinates of microphone 3
    ]

    # Assuming 2D space
    actual_pos = [2.5, 3.5, 10.0]

    actual_pos = np.array(actual_pos)

    # Calculate distances from the actual position to each microphone
    distances = [np.linalg.norm(actual_pos - np.array(mic))
                 for mic in mic_positions]

    distances = np.array(distances) - distances[0]  # Normalize distances

    mics = [Microphone(dist, np.array(pos))
            for dist, pos in zip(distances, mic_positions)]

    # Initial guess for the sound source position
    initial_guess = np.array([0.0, 0.0, 0.0])

    start_time = time.time()
    estimated_pos = find_sound_source(mics, initial_guess)
    print(f"Estimated sound source position: {estimated_pos}")
    print(f"Time taken: {time.time() - start_time} seconds")
