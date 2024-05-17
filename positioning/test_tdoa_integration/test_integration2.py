from positioning.tdoa import TDOAMethod
from positioning.calcfunctions.receiver import Receiver
import numpy as np


ERROR_MARGIN: float = 0.5


def calculate_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points in n-dimensional space.

    Args:
        point1 (list[float]): Coordinates of the first point.
        point2 (list[float]): Coordinates of the second point.

    Returns:
        float: The Euclidean distance between the two points.
    """
    # Convert lists to numpy arrays
    point1 = np.array(point1)
    point2 = np.array(point2)

    # Calculate the Euclidean distance using numpy's linalg.norm function
    distance = np.linalg.norm(point1 - point2)
    return distance


def assert_positioning(test_id, mic_positions, true_source, algorithm='gradient'):
    """
    Test the positioning system for a given test scenario.

    Args:
        test_id (int): ID of the test scenario, used to determine which audio files to load.
        mic_positions (list[list[float]]): Positions of the microphones.
        true_source (list[float]): The true position of the source.
        algorithm (str): The algorithm to use for positioning, either 'gradient' or 'grid'.

    Raises:
        AssertionError: If the estimated source position is not within the acceptable range of the true source.
    """
    method = TDOAMethod()
    # Set the algorithm to use for the method
    method.set_setting("algorithm", algorithm)

    # Build the microphone data dictionary with file paths
    microphones_data = {
        Receiver(position): f"test_tdoa_integration/scenario_{test_id}/microphone_{idx+1}.wav"
        for idx, position in enumerate(mic_positions)
    }

    # Find source using the method's implementation
    estimated_source = method.find_source(microphones_data)
    print(f"Estimated Source for Test ID {test_id} using '{
          algorithm}': {estimated_source}")

    # Calculate the Euclidean distance to assert proximity to true source
    assert calculate_distance(
        estimated_source, true_source) < ERROR_MARGIN, "Estimated source too far from true source"


def test_positioning_gradient_id_1():
    assert_positioning(test_id=1, mic_positions=[
                       [0, 0], [0, 15], [13, 7.5]], true_source=[0, 0], algorithm='gradient')


def test_positioning_grid_id_1():
    assert_positioning(test_id=1, mic_positions=[
                       [0, 0], [0, 15], [13, 7.5]], true_source=[0, 0], algorithm='grid')


def test_positioning_gradient_id_4():
    assert_positioning(test_id=4, mic_positions=[
                       [0, 0], [0, 15], [13, 7.5]], true_source=[4.3, 7.5], algorithm='gradient')


def test_positioning_grid_id_4():
    assert_positioning(test_id=4, mic_positions=[
                       [0, 0], [0, 15], [13, 7.5]], true_source=[4.3, 7.5], algorithm='grid')


def test_positioning_gradient_id_6():
    assert_positioning(test_id=6, mic_positions=[
                       [0, 0], [0, 15], [13, 7.5]], true_source=[0, 7.5], algorithm='gradient')


def test_positioning_grid_id_6():
    assert_positioning(test_id=6, mic_positions=[
                       [0, 0], [0, 15], [13, 7.5]], true_source=[0, 7.5], algorithm='grid')


def test_positioning_gradient_id_9():
    assert_positioning(test_id=9, mic_positions=[
                       [0, 0], [0, 25], [21.5, 12.5]], true_source=[0, 0], algorithm='gradient')


def test_positioning_grid_id_9():
    assert_positioning(test_id=9, mic_positions=[
                       [0, 0], [0, 25], [21.5, 12.5]], true_source=[0, 0], algorithm='grid')


def test_positioning_gradient_id_13():
    assert_positioning(test_id=13, mic_positions=[
                       [0, 0], [0, 25], [21.5, 12.5]], true_source=[10, 0], algorithm='gradient')


def test_positioning_grid_id_13():
    assert_positioning(test_id=13, mic_positions=[
                       [0, 0], [0, 25], [21.5, 12.5]], true_source=[10, 0], algorithm='grid')


def test_positioning_gradient_id_25():
    assert_positioning(test_id=25, mic_positions=[
                       [0, 0, 0], [0, 30, 5.3], [30, 30, 0], [30, 0, 5.3]], true_source=[15, 15, 0], algorithm='gradient')


def test_positioning_grid_id_25():
    assert_positioning(test_id=25, mic_positions=[
                       [0, 0, 0], [0, 30, 5.3], [30, 30, 0], [30, 0, 5.3]], true_source=[15, 15, 0], algorithm='grid')


def test_positioning_gradient_id_27():
    assert_positioning(test_id=27, mic_positions=[
                       [0, 0, 0], [0, 30, 5.3], [30, 30, 0], [30, 0, 5.3]], true_source=[10, 0, 0], algorithm='gradient')


def test_positioning_grid_id_27():
    assert_positioning(test_id=27, mic_positions=[
                       [0, 0, 0], [0, 30, 5.3], [30, 30, 0], [30, 0, 5.3]], true_source=[10, 0, 0], algorithm='grid')


def test_positioning_gradient_id_35():
    assert_positioning(test_id=35, mic_positions=[
                       [0, 0, 0], [0, 30, 5.3], [30, 30, 0], [30, 0, 5.3]], true_source=[35, 35, 0], algorithm='gradient')


def test_positioning_grid_id_35():
    assert_positioning(test_id=35, mic_positions=[
                       [0, 0, 0], [0, 30, 5.3], [30, 30, 0], [30, 0, 5.3]], true_source=[35, 35, 0], algorithm='grid')
