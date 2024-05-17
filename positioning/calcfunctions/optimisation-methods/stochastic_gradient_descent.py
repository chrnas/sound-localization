import numpy as np
import time


class Microphone:
    def __init__(self, distance, coords):
        self.distance = distance  # Relative distance from the first microphone
        self.coords = np.array(coords)


def stochastic_residual(x, mic):
    # Compute the residual for a single, randomly selected microphone
    return np.linalg.norm(x - mic.coords) - mic.distance


def sgd_step(x, mics, learning_rate=0.01):
    # Randomly select a microphone
    mic = np.random.choice(mics)
    # Compute the gradient of the stochastic residual
    residual = stochastic_residual(x, mic)
    grad = (x - mic.coords) * residual / np.linalg.norm(x - mic.coords)
    # Update the estimated position
    x_new = x - learning_rate * grad
    return x_new


def find_sound_source(mics, initial_guess, iterations=10000000):
    estimated_pos = initial_guess
    for _ in range(iterations):
        estimated_pos = sgd_step(estimated_pos, mics)
    return estimated_pos


if __name__ == "__main__":
    mic_positions = [
        [10.0, 2.0, 0],    # Coordinates of microphone 1
        [3.0, 0.0, 15],  # Coordinates of microphone 2
        [15.0, 6.0, 10],   # Coordinates of microphone 3
    ]

    # Actual position of the sound source
    actual_pos = np.array([2.0, 0, 5.0])

    distances = [np.linalg.norm(actual_pos - np.array(mic))
                 for mic in mic_positions]
    distances = np.array(distances) - distances[0]  # Normalize distances

    mics = [Microphone(dist, np.array(pos))
            for dist, pos in zip(distances, mic_positions)]

    initial_guess = np.random.uniform(
        low=-15, high=15, size=(3,))  # Example for 3D coordinates

    start_time = time.time()
    estimated_pos = find_sound_source(mics, initial_guess)
    print(f"Estimated sound source position: {estimated_pos}")
    print(f"Time taken: {time.time() - start_time} seconds")
