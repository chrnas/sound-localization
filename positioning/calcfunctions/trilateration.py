import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import minimize
from typing import Union
import sympy as sp
import time
import os
from .symbolic_helpers import load_expression
from .receiver import Receiver


class MicrophoneArray:
    """
    Manages an array of microphones, including functionality to calculate time differences,
    estimate source positions, and evaluate cost functions.
    """

    def __init__(self, items: list[Union[np.ndarray, list, Receiver]]):
        """
        Initialize a MicrophoneArray with a list of positions.

        Args:
            positions (list[np.ndarray]): Positions of microphones in the array.
        """
        if all(isinstance(item, np.ndarray) or isinstance(item, list) for item in items):
            # If items are arrays or lists, create new Receiver objects
            self.microphones = [Receiver(pos) for pos in items]
        elif all(isinstance(item, Receiver) for item in items):
            # If items are Receiver objects, add them directly
            self.microphones = items
        else:
            raise ValueError(
                "All items must be either lists, numpy arrays, or Receiver instances.")
        self.cost_function = None
        self.gradient_functions = None
        self.hessian_function = None

    def calculate_time_diffs(self, source_pos: Union[list, np.ndarray], speed_of_sound: float = 343) -> None:
        """
        Calculates what the time differences should be an all of the microphones given some time difference and the speed of sound. This function should and can only be used for testing purposes.

        Args:
            source_pos (Union[list, np.ndarray]): The position of the sound source.
            speed_of_sound (float): The speed of sound used in the calculations (default: 343 m/s).
        """

        source_pos = np.array(
            source_pos)  # Ensure source position is an ndarray.

        self.order_microphones_by_distance(source_pos=source_pos)

        pairs = self.generate_pairs_with_first()
        # Time difference for the first microphone is always zero.
        self.microphones[0].set_time_difference(0.0)
        for first_mic, mic in pairs:
            distance = np.linalg.norm(source_pos - mic.get_position())
            reference_distance = np.linalg.norm(
                source_pos - first_mic.get_position())
            time_diff = (distance - reference_distance) / speed_of_sound
            mic.set_time_difference(time_diff)

    def order_microphones_by_distance(self, source_pos: np.ndarray) -> None:
        """
        Orders the microphones in the class based on their distances from the source position.

        Args:
            source_pos (np.ndarray): The position of the sound source.
        """
        self.microphones.sort(key=lambda mic: np.linalg.norm(
            source_pos - mic.get_position()))

    def get_microphones(self) -> list[Receiver]:
        """
        Retrieve a list of microphones in the array.

        Returns:
            list[Microphone]: List of microphones.
        """
        return self.microphones

    def get_num_dimensions(self) -> int:
        """
        Determine the number of dimensions of the space based on the first microphone.

        Returns:
            int: Number of dimensions.
        """

        return len(self.microphones[0].get_position())

    def get_num_microphones(self) -> int:
        """
        Retrieve the number of microphones in the array.

        Returns:
            int: Number of microphones.
        """
        return len(self.microphones)

    def generate_pairs_with_first(self) -> list[tuple[Receiver, Receiver]]:
        """
        Generate pairs of the first microphone with each of the other microphones.

        Returns:
            list[tuple[Microphone, Microphone]]: A list of tuples, each containing the first microphone and another microphone.
        """
        first_mic = self.microphones[0]
        return [(first_mic, mic) for mic in self.microphones[1:]]

    def add_microphones(self, mics: Union[Receiver, list[Receiver]]) -> None:
        """
        Adds one or more microphones to the array and sorts all microphones by time difference.

        Args:
            mics (Union[Microphone, list[Microphone]]): A single Microphone instance or a list of Microphone instances.
        """
        if isinstance(mics, Receiver):
            self.microphones.append(mics)
        elif isinstance(mics, list):
            self.microphones.extend(mics)
        else:
            raise TypeError(
                "Input must be a Microphone instance or a list of Microphone instances.")

        # Sort microphones by their time differences
        self.microphones.sort(key=lambda mic: mic.get_time_difference())

    def estimate_position(self, tolerance_of_termination: float = 1e-5) -> tuple[np.ndarray, float]:
        """
        Estimate the position of the sound source using optimization methods based on the microphone array setup.

        Args:
            tolerance_of_termination (float): The tolerance for termination of the optimization process.

        Returns:
            tuple[np.ndarray, float]: A tuple containing the estimated position of the sound source
                                       and the minimized cost function value.
        """
        self.create_dynamic_cost_function()
        
        [print(microphone.get_time_difference())
         for microphone in self.get_microphones()]

        initial_guesses = np.mean([mic.get_position()
                                  for mic in self.get_microphones()], axis=0)
        result = minimize(
            self.evaluate_cost, initial_guesses, tol=tolerance_of_termination,
            method='trust-krylov', jac=self.evaluate_gradient, hess=self.evaluate_hessian
        )

        return result.x, result.fun

    def plot_cost_function(self, actual_pos: np.ndarray, estimated_pos: np.ndarray) -> None:
        """
        Plot the 3D surface of the cost function, highlighting the positions of the microphones,
        the actual sound source, and the estimated position.

        Args:
            actual_pos (np.ndarray): The actual position of the sound source.
            estimated_pos (np.ndarray): The estimated position of the sound source as determined by the optimization.
        """
        x_grid, y_grid = np.meshgrid(
            np.arange(-50, 50, 2), np.arange(-50, 50, 2))
        z = np.array([[self.evaluate_cost(np.array([x, y])) for x, y in zip(
            x_row, y_row)] for x_row, y_row in zip(x_grid, y_grid)])

        fig, ax = plt.subplots()
        # Create a heatmap (or contour map) of the cost function values
        c = ax.contourf(x_grid, y_grid, z, cmap='viridis', levels=50)
        fig.colorbar(c, ax=ax, label='Kostnad värde (J)')

        # Flag to add label only once
        label_added = False

        # Plotting crosses at the microphone positions
        for mic in self.microphones:
            mic_pos = mic.get_position()
            if not label_added:
                ax.plot(mic_pos[0], mic_pos[1], 'bx', markersize=10)
                label_added = True
            else:
                ax.plot(mic_pos[0], mic_pos[1], 'bx', markersize=10)

        # Plotting and labeling the actual position cross
        # ax.plot(actual_pos[0], actual_pos[1], 'rx', markersize=12, label='Actual Position')

        # Plotting and labeling the estimated position cross
        ax.plot(estimated_pos[0], estimated_pos[1], 'gx', markersize=12,)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('2D Heatmap of the Cost Function')
        plt.legend()
        plt.show()

    def create_dynamic_cost_function(self):
        dimensions = self.get_num_dimensions()
        num_mics = self.get_num_microphones()
        base_filename = f"{dimensions}d_{num_mics}mics"

        # Directory and filenames for each type of function
        cost_dir = "cost_functions"
        gradient_dir = "gradient_functions"
        hessian_dir = "hessian_functions"

        cost_file = os.path.join(
            cost_dir, f"cost_function_{base_filename}.txt")
        gradient_file = os.path.join(
            gradient_dir, f"gradient_function_{base_filename}.txt")
        hessian_file = os.path.join(
            hessian_dir, f"hessian_function_{base_filename}.txt")

        # Load expressions
        cost_expr = load_expression(cost_file)
        gradients_expr = load_expression(gradient_file)
        hessian_expr = load_expression(hessian_file)

        # Define the necessary symbols for evaluation
        symbols = sp.symbols(
            ' '.join(['x{}'.format(i) for i in range(dimensions)]))
        speed_of_sound = sp.Symbol('speed_of_sound')
        mic_positions = sum([sp.symbols(' '.join(['x{}_mic{}'.format(
            i, mic) for i in range(dimensions)])) for mic in range(num_mics)], ())
        time_diffs = [sp.Symbol('t_mic{}'.format(mic))
                      for mic in range(num_mics)]
        all_params = symbols + (speed_of_sound,) + \
            mic_positions + tuple(time_diffs)

        # sp.pprint(hessian_expr)

        # Convert the symbolic expressions to callable functions
        modules = [{'ImmutableMatrix': np.array,
                    'MutableDenseMatrix': np.array}, 'numpy']
        self.cost_function = sp.lambdify(
            all_params, cost_expr, modules=modules)
        self.gradient_functions = sp.lambdify(
            all_params, gradients_expr, modules=modules)
        self.hessian_function = sp.lambdify(
            all_params, hessian_expr, modules=modules)

    def create_dynamic_cost_function_old(self):
        """
        Dynamically create the cost, gradient, and hessian functions using symbolic computation
        based on the current configuration of microphones.

        Returns: None

        """
        dimensions = self.get_num_dimensions()
        num_mics = self.get_num_microphones()
        position_symbols = sp.symbols(
            ' '.join(['x{}'.format(i) for i in range(dimensions)]))
        speed_of_sound = sp.Symbol('speed_of_sound')

        mic_positions = [sp.symbols(' '.join(['x{}_mic{}'.format(
            i, mic) for i in range(dimensions)])) for mic in range(num_mics)]
        time_diffs = [sp.Symbol('t_mic{}'.format(mic))
                      for mic in range(num_mics)]

        guess_pos = sp.Matrix(position_symbols)
        cost_expr = 0
        first_mic_pos = sp.Matrix(mic_positions[0])

        for pos, time_diff in zip(mic_positions[1:], time_diffs[1:]):
            mic_pos = sp.Matrix(pos)
            distance = sp.sqrt((guess_pos - mic_pos).dot(guess_pos - mic_pos))
            distance_from_first = sp.sqrt(
                (guess_pos - first_mic_pos).dot(guess_pos - first_mic_pos))
            time_term = speed_of_sound * time_diff
            cost_component = (distance - distance_from_first - time_term)**2
            cost_expr += cost_component

        gradients = [cost_expr.diff(var) for var in position_symbols]
        hessian = sp.Matrix([[cost_expr.diff(var1, var2)
                            for var1 in position_symbols] for var2 in position_symbols])

        all_positions = sum(mic_positions, ())
        all_params = position_symbols + \
            (speed_of_sound,) + all_positions + tuple(time_diffs)

        modules = [{'ImmutableMatrix': np.array,
                    'MutableDenseMatrix': np.array}, 'numpy']
        cost_func = sp.lambdify(all_params, cost_expr, modules=modules)
        gradient_funcs = sp.lambdify(all_params, gradients, modules=modules)
        hessian_func = sp.lambdify(all_params, hessian, modules=modules)

        self.cost_function = cost_func

        self.gradient_functions = gradient_funcs

        self.hessian_function = hessian_func

    def evaluate_cost(self, guess_pos, speed_of_sound: float = 343) -> float:
        """
        Evaluate the cost function at a given position and speed of sound.

        Args:
            guess_pos (np.ndarray): The position at which to evaluate the cost.
            speed_of_sound (float): The speed of sound used in the computation.

        Returns:
            float: The evaluated cost at the specified position.
        """
        params = {
            'speed_of_sound': speed_of_sound,
            **{f'x{i}': guess_pos[i] for i in range(len(guess_pos))},
            **{f'x{i}_mic{j}': self.microphones[j].get_position()[i] for j in range(len(self.microphones)) for i in range(len(guess_pos))},
            **{f't_mic{j}': self.microphones[j].get_time_difference() for j in range(len(self.microphones))}
        }
        return self.cost_function(**params)

    def evaluate_gradient(self, guess, speed_of_sound: float = 343) -> np.ndarray:
        """
        Evaluate the gradient of the cost function at a given position.

        Args:
            guess (np.ndarray): The position at which to evaluate the gradient.
            speed_of_sound (float): The speed of sound used in the computation.

        Returns:
            np.ndarray: The gradient vector of the cost function at the specified position.
        """
        params = {
            'speed_of_sound': speed_of_sound,
            **{f'x{i}': guess[i] for i in range(len(guess))},
            **{f'x{i}_mic{j}': self.microphones[j].get_position()[i] for j in range(len(self.microphones)) for i in range(len(guess))},
            **{f't_mic{j}': self.microphones[j].get_time_difference() for j in range(len(self.microphones))}
        }
        gradient_vector = self.gradient_functions(**params)
        return np.array(gradient_vector)

    def evaluate_hessian(self, guess, speed_of_sound: float = 343) -> np.ndarray:
        """
        Evaluate the Hessian matrix of the cost function at a given position.

        Args:
            guess (np.ndarray): The position at which to evaluate the Hessian.
            speed_of_sound (float): The speed of sound used in the computation.

        Returns:
            np.ndarray: The Hessian matrix at the specified position.
        """
        params = {
            'speed_of_sound': speed_of_sound,
            **{f'x{i}': guess[i] for i in range(len(guess))},
            **{f'x{i}_mic{j}': self.microphones[j].get_position()[i] for j in range(len(self.microphones)) for i in range(len(guess))},
            **{f't_mic{j}': self.microphones[j].get_time_difference() for j in range(len(self.microphones))}
        }
        hessian_matrix = self.hessian_function(**params)
        return np.array(hessian_matrix)


if __name__ == "__main__":
    # Define a list of microphone positions
    microphone_list = [[0, 0, 0], [0, 30, 5.5], [
        30, 30, 0], [30, 0, 5.5], [15, 15, 0]]
    microphone_array = MicrophoneArray(microphone_list)

    # Define the sound source position
    sound_source = np.array([150, 1, 20.5])
    microphone_array.calculate_time_diffs(source_pos=sound_source)

    # Estimate the position of the sound source and compute its cost
    estimated_position, function_value = microphone_array.estimate_position()
    print(f"Estimated Position: {
          estimated_position}, Function Value: {function_value}")
    print(f"Distance from Actual Source: {
          np.linalg.norm(estimated_position - sound_source)}")
    print(f"Cost of Estimated Position: {microphone_array.evaluate_cost(
        estimated_position)}, Cost of Actual Position: {microphone_array.evaluate_cost(sound_source)}")

    # Plot the cost function with actual and estimated positions
    # microphone_array.plot_cost_function(
    #    actual_pos=sound_source, estimated_pos=estimated_position)
