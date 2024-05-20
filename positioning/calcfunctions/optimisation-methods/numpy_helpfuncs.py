import numpy as np
import time


class Microphone:

    def __init__(self, distance, coords):
        self.distance = distance
        self.coords = np.array(coords)


class TravelSettings:

    def __init__(self, dimensions, step):
        self.dimensions = dimensions  # Number of dimensions the settings are for
        # Smallest coordinates to always include
        self.smallest_start = np.zeros(dimensions)
        # Biggest coordinates to always include
        self.biggest_start = np.zeros(dimensions)
        # How far outside mic area to search in negative coords
        self.smallest_expansion = np.ones(dimensions)
        # How far outside mic area to search in positive coords
        self.biggest_expansion = np.ones(dimensions)
        self.step = step  # How far to travel between each search point


def get_error(coords, mics):
    error = 0
    previous_mic = mics[-1]
    for mic in mics:
        current_dist = np.linalg.norm(coords - mic.coords)
        previous_dist = np.linalg.norm(coords - previous_mic.coords)

        left_side = current_dist - previous_dist
        right_side = mic.distance - previous_mic.distance

        error += abs(left_side - right_side)

    return error


def travel_grid(mics, smallest, biggest, step):
    best_error = float("inf")
    best_pos = mics[0].coords.copy()
    positions = smallest.copy()

    while True:
        current_error = get_error(positions, mics)
        if best_error > current_error:
            best_pos = positions.copy()
            best_error = current_error

        for i in range(len(positions)):
            positions[i] += step
            if positions[i] > biggest[i]:
                positions[i] = smallest[i]
            else:
                break

        if np.array_equal(positions, smallest):
            break

    return best_pos


def find_sound_source(mics, settings):
    smallest = np.array(settings.smallest_start)
    biggest = np.array(settings.biggest_start)

    for mic in mics:
        smallest = np.minimum(smallest, mic.coords)
        biggest = np.maximum(biggest, mic.coords)

    smallest -= settings.smallest_expansion
    biggest += settings.biggest_expansion

    best_pos = travel_grid(mics, smallest, biggest, settings.step)
    return best_pos


def get_distance(sound_pos, mic_pos):
    return np.linalg.norm(sound_pos - mic_pos)


if __name__ == "__main__":
    mic_positions = [
        [10.0, 2.0, 0],  # Coordinates of microphone 1
        [3.0, -25.0, 15],  # Coordinates of microphone 2
        [25.0, 6.0, 10],  # Coordinates of microphone 3
    ]

    step = 0.5  # Hardcoded accuracy
    settings = TravelSettings(3, step)  # Assuming 2D space

    # Hardcoded search expansions
    expansion_negative = 1  # Negative search expansion
    expansion_positive = 1  # Positive search expansion
    settings.smallest_expansion = np.full(
        settings.dimensions, expansion_negative)
    settings.biggest_expansion = np.full(
        settings.dimensions, expansion_positive)

    # Hardcoded actual position of the sound source, converted to NumPy array
    actual_pos = [2.5, 3.5, 10.0]

    start_time = time.time()

    # Calculate distances from the actual position to each microphone
    # Ensure mic_positions are converted to NumPy arrays
    distances = [get_distance(actual_pos, np.array(mic))
                 for mic in mic_positions]
    distances = np.array(distances) - distances[0]  # Normalize distances

    mics = [Microphone(dist, pos)
            for dist, pos in zip(distances, mic_positions)]

    result_pos = find_sound_source(mics, settings)
    print(f"Estimated sound source position: {result_pos}")
    print(f"Time taken: {time.time() - start_time} seconds")
