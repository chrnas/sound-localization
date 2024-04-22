import numpy as np
import time
from scipy.optimize import differential_evolution


class Microphone:
    def __init__(self, distance, coords):
        self.distance = distance  # Relative distance from the first microphone
        self.coords = np.array(coords)


def objective_function(x, mics):
    return sum((np.linalg.norm(x - mic.coords) - mic.distance) ** 2 for mic in mics)


def find_sound_source(mics, bounds):
    result = differential_evolution(objective_function, bounds, args=(mics,))
    return result.x


if __name__ == "__main__":
    mic_positions = [
        [10.0, 2.0, 0],    # Coordinates of microphone 1
        [3.0, 25.0, 15],  # Coordinates of microphone 2
        [25.0, 6.0, 10],   # Coordinates of microphone 3
    ]

    # Assuming 3D space
    # Actual position of the sound source
    actual_pos = np.array([0, 0, 0])

    # Calculate distances from the actual position to each microphone
    distances = [np.linalg.norm(actual_pos - np.array(mic))
                 for mic in mic_positions]
    distances = np.array(distances) - distances[0]  # Normalize distances

    mics = [Microphone(dist, np.array(pos))
            for dist, pos in zip(distances, mic_positions)]

    # Bounds for the sound source position (you might need to adjust these based on your problem space)
    # Assuming the sound source can be within a 100x100x100 cube
    bounds = [(-50, 50), (-50, 50), (-50, 50)]

    start_time = time.time()
    estimated_pos = find_sound_source(mics, bounds)
    print(f"Estimated sound source position: {estimated_pos}")
    print(f"Time taken: {time.time() - start_time} seconds")
