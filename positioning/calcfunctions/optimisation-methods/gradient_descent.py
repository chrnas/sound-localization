import numpy as np
import time
from scipy.optimize import minimize


class Microphone:
    def __init__(self, distance, coords):
        self.distance = distance
        self.coords = np.array(coords)


def objective_function(x, mics):
    # Sum of squared residuals
    return sum((np.linalg.norm(x - mic.coords) - mic.distance) ** 2 for mic in mics)


def find_sound_source(mics, initial_guess):
    result = minimize(objective_function, initial_guess,
                      args=(mics,), method='')
    return result.x


if __name__ == "__main__":
    mic_positions = [
        [5.0, 2.0, 0],    # Coordinates of microphone 1
        [3.0, 25.0, 15],  # Coordinates of microphone 2
        [10.0, 6.0, 10],   # Coordinates of microphone 3
    ]

    # Assuming 3D space
    # Actual position of the sound source
    actual_pos = np.array([2.5, 3.5, 5.0])

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
