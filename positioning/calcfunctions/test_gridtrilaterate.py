from .gridtrilaterate import get_distance, GridTravelSettings, trilaterate_grid
from .receiver import Receiver as receiver
import time


def create_mics(actual_pos, mic_positions):
    distances = [get_distance(
        actual_pos, mic) for mic in mic_positions]
    first_dist = distances[0]
    for dist in distances:
        dist -= first_dist
    mics = receiver.create_mics(mic_positions)
    for i in range(len(mic_positions)):
        mics[i].set_distance_difference(distances[i])
    return mics


STEP = 1  # How small steps to take [m]
EXPANSION = 5  # How much to expand the search area [m]
TIME_LIMIT = 1.5  # Acceptable time for the function to run [s]
# Acceptable difference between actual and calculated position [m]
ACCURACY = 1


def test_1_8():
    """
    Testing cases 1-8 from "Datainsamlingsplan 4/4". Coordinates are round to closest 0.5.
    """
    mic_positions = [[0, 0], [0, 15], [13, 7.5]]
    settings = GridTravelSettings(len(mic_positions[0]), STEP)
    settings.smallest_expansion = [
        EXPANSION for i in settings.smallest_expansion]
    settings.biggest_expansion = [
        EXPANSION for i in settings.smallest_expansion]

    start_time = time.time()
    actual_pos = [0, 0]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [0, 15]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [13, 7.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [4.5, 7.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [10, 0]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [0, 7.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [5, 5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [3, 10]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT


def test_9_16():
    """
    Testing cases 9-16 from "Datainsamlingsplan 4/4". Coordinates are round to closest 0.5.
    """
    mic_positions = [[0, 0], [0, 25], [21.5, 12.5]]
    settings = GridTravelSettings(len(mic_positions[0]), STEP)
    settings.smallest_expansion = [
        EXPANSION for i in settings.smallest_expansion]
    settings.biggest_expansion = [
        EXPANSION for i in settings.smallest_expansion]

    start_time = time.time()
    actual_pos = [0, 0]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [0, 25]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [21.5, 12.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [7, 12.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [10, 0]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [0, 10]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [4, 11]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [13, 13]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT


def test_17_24():
    """
    Testing cases 17-24 from "Datainsamlingsplan 4/4". Coordinates are round to closest 0.5.
    """
    mic_positions = [[0, 0], [0, 35], [30.5, 17.5]]
    settings = GridTravelSettings(len(mic_positions[0]), STEP)
    settings.smallest_expansion = [
        EXPANSION for i in settings.smallest_expansion]
    settings.biggest_expansion = [
        EXPANSION for i in settings.smallest_expansion]

    start_time = time.time()
    actual_pos = [0, 0]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [0, 35]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [30.5, 17.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [10, 17.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [10, 0]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [0, 10]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [17.5, 17.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [3, 27]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT


def test_25_36():
    """
    Testing cases 25-36 from "Datainsamlingsplan 4/4". Coordinates are round to closest 0.5.
    """
    mic_positions = [[0, 0, 0], [0, 30, 5.5], [30, 30, 0], [30, 0, 5.5]]
    settings = GridTravelSettings(len(mic_positions[0]), STEP)
    settings.smallest_expansion = [
        EXPANSION for i in settings.smallest_expansion]
    settings.biggest_expansion = [
        EXPANSION for i in settings.smallest_expansion]

    start_time = time.time()
    actual_pos = [15, 15, 0]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [15, 15, 2.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [10, 0, 0]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [10, 0, 2.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [0, 30, 0]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [0, 30, 2.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [25, 20, 0]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [25, 20, 2.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [5, 20, 0]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [5, 20, 2.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [35, 35, 0]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [35, 35, 2.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT


def test_5_mics():
    """
    Testing some cases with 5 microphones.
    """
    mic_positions = [[0, 0, 0], [0, 30, 5.5], [
        30, 30, 0], [30, 0, 5.5], [15, 15, 0]]
    settings = GridTravelSettings(len(mic_positions[0]), STEP)
    settings.smallest_expansion = [
        EXPANSION for i in settings.smallest_expansion]
    settings.biggest_expansion = [
        EXPANSION for i in settings.smallest_expansion]

    start_time = time.time()
    actual_pos = [35, 35, 2.5]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [-1, -1, 0]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT

    start_time = time.time()
    actual_pos = [15, 15, 0]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = trilaterate_grid(mics, settings)
    assert sum(resultpos) - sum(actual_pos) <= ACCURACY
    assert time.time() - start_time < TIME_LIMIT
