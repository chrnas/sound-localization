"""
This file contains the data collection for quality metrics related to the
system.
"""

# Needed to be able to import from parent directory
import sys
import os
dirname = os.path.dirname(__file__)
root_path = os.path.join(dirname, "../")
sys.path.append(root_path)

import pytest
from math import sqrt, pow
from datetime import datetime, timedelta
from system_tests.fake_data.generate_differences import (
    Point,
    Scenario
)
from system_tests.fake_data.scenarios import (
    SCENARIOS_2D,
    SCENARIOS_3D,
)
import positioning.tdoa as tdoa
from positioning.calcfunctions.receiver import Receiver


@pytest.mark.skip  # Not implemented
def test_2d_error():
    """
    Id: 1
    Quality requirement: 3.5.2
    Dependencies: This test requires that atleast one method for locating
    sounds has been implemented.
    Tests: This test collects metrics on the margin of error when locating
    sounds in two dimensions.
    """
    folders = os.path.join(os.path.dirname(__file__), "fake_data/audio_2d")
    assert len([0 for scenario, folder in zip(SCENARIOS_2D, folders) if
                within_2d_error(scenario, folder)]) / len(folders) >= 0.8


@pytest.mark.skip  # Not implemented
def test_3d_error():
    """
    Id: 2
    Quality requirement: 3.5.4
    Dependencies: This test requires that atleast one method for locating
    sounds has been implemented. It also requires the system pipeline is
    implemented in order to correctly measure the delay between data input to
    data output.
    Tests: This test collects metrics on the total delay from inputted sounds
    to outputted position.
    """
    folders = os.path.join(os.path.dirname(__file__), "fake_data/audio_3d")
    assert len([0 for scenario, folder in zip(SCENARIOS_3D, folders) if
                within_3d_error(scenario, folder)]) / len(folders) >= 0.75


@pytest.mark.skip  # Not implemented
def test_delay():
    """
    Id: 3
    Quality requirement: 3.5.3
    Dependencies: This test requires that atleast one method for locating
    sounds has been implemented.
    Tests: This test collects metrics on the margin of error when locating
    sounds in three dimensions. This in relation to a horizontal x and y
    plane, as well as a vertical axis z.
    """
    folders_2d = os.path.join(os.path.dirname(__file__), "fake_data/audio_2d")
    folders_3d = os.path.join(os.path.dirname(__file__), "fake_data/audio_3d")
    folders = folders_2d + folders_3d
    assert len([0 for folder in folders if
                within_allowed_time(folder)]) / len(folders) >= 0.8

# Helper functions


def get_abs_path(relative_path):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), relative_path))


def point_to_2d(point: Point):
    return [point.x, point.y]


def point_to_3d(point: Point):
    return [point.x, point.y, point.z]


def data2d_from_scenario(scenario: Scenario, folder: str):
    audio_files = os.listdir(folder)
    return {Receiver(point_to_2d(receiver)):
            get_abs_path(f"{folder}/{audio_file}") for
            receiver, audio_file in zip(scenario.receivers, audio_files)}


def data3d_from_scenario(scenario: Scenario, folder: str):
    audio_files = os.listdir(folder)
    return {Receiver(point_to_3d(receiver)):
            get_abs_path(f"{folder}/{audio_file}") for
            receiver, audio_file in zip(scenario.receivers, audio_files)}


def distance(source: tuple[float, float, float],
             guess: tuple[float, float, float]):
    """
    Checks distance between a source of a sound and a guess.
    """
    x_diff = source[0] - guess[0]
    y_diff = source[1] - guess[1]
    z_diff = source[2] - guess[2]
    return sqrt(pow(x_diff, 2) + pow(y_diff, 2) + pow(z_diff, 2))


def within_2d_error(scenario: Scenario, folder: str):
    """
    Quality requirement: 3.5.2
    Verifies that a guessed postion is within the allowed margin of error for
    the 2d plane.
    """
    method = tdoa.TDOAMethod()
    method.set_setting("algorithm", "gradient")
    source = scenario.sender
    data = data2d_from_scenario(scenario, folder)
    start_time = datetime.now()
    guess = method.find_source(data)
    end_time = datetime.now()
    microphone_distance = scenario.receivers[0].distance(scenario.receivers[1])
    source_no_z = (source.x, source.y, 0)
    guess_no_z = (guess[0], guess[1], 0)
    accepted = distance(source_no_z, guess_no_z) <= microphone_distance * 0.2
    return accepted, end_time - start_time, distance(source_no_z, guess_no_z)


def within_3d_error(scenario: Scenario, folder: str):
    """
    Quality requirement: 3.5.4
    Verifies that a guessed postion is within the allowed margin of error for
    three dimensions.
    """
    method = tdoa.TDOAMethod()
    method.set_setting("algorithm", "gradient")
    _source = scenario.sender
    data = data3d_from_scenario(scenario, folder)
    start_time = datetime.now()
    _guess = method.find_source(data)
    end_time = datetime.now()
    source = (_source.x, _source.y, _source.z)
    guess = (_guess[0], _guess[1], _guess[2])
    accepted = distance(source, guess) <= 5
    return accepted, end_time - start_time, distance(source, guess)


def within_allowed_time(scenario: Scenario, folder: str):
    """
    Quality requirement: 3.5.3
    Verifies that a answer is given within the allowed time.
    """
    start = datetime.now()
    # audio_files = os.listdir(folder)
    # TODO: guess_pos(data) # perform guess
    return datetime.now() - start <= timedelta(seconds=0.5)


if __name__ == "__main__":
    os.listdir(os.path.dirname(__file__))
    # When collecting metrics this is run instead of the pytest tests.
    path_2d = "fake_data/audio_2d/"
    path_3d = "fake_data/audio_3d/"
    folders_2d = os.listdir(get_abs_path(path_2d))
    folders_2d.sort(key=lambda x: float(x.strip('scenario_')))
    folders_3d = os.listdir(get_abs_path(path_3d))
    folders_3d.sort(key=lambda x: float(x.strip('scenario_')))
    folders = folders_2d + folders_3d

    res_2d = [within_2d_error(scenario, get_abs_path(path_2d + folder))
              for scenario, folder in zip(SCENARIOS_2D, folders_2d)]
    res_3d = [within_3d_error(scenario, get_abs_path(path_3d + folder))
              for scenario, folder in zip(SCENARIOS_3D, folders_3d)]
    res_delay = [0 for _, delay, _ in res_2d + res_3d
                 if delay <= timedelta(seconds=0.5)]

    pass_2d_percentage = len([0 for x in res_2d if x[0]]
                             ) / len(folders_2d) * 100
    pass_3d_percentage = len([0 for x in res_3d if x[0]]
                             ) / len(folders_3d) * 100
    pass_delay_percentage = len(res_delay) / len(folders) * 100

    average_error_2d = sum([error for _, _, error in res_2d]) / len(res_2d)
    average_error_3d = sum([error for _, _, error in res_3d]) / len(res_3d)
    average_delay_2d = sum([delay for _, delay, _ in res_2d], timedelta()) / len(res_2d)
    average_delay_3d = sum([delay for _, delay, _ in res_3d], timedelta()) / len(res_3d)

    print("Quality metrics:")
    print(f"Within 20% of the distance between microphones in a 2d plane, {
          pass_2d_percentage}% of the time.")
    print(f"Within 5 meters in a 3d space, {pass_3d_percentage}% of the time.")
    print(f"Gives a postion within 0.5s, {
          pass_delay_percentage}% of the time.")
    print("")
    print("Metrics:")
    print(f"Average 2d error: {average_error_2d}m")
    print(f"Average 3d error: {average_error_3d}m")
    print(f"Average 2d delay: {average_delay_2d}s")
    print(f"Average 3d delay: {average_delay_3d}s")
