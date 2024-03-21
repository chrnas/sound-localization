"""
This file contains the data collection for quality metrics related to the system.
"""

# TODO: add pytest, test id's
# TODO: This file assumes output is given in meters

import pytest
from math import sqrt, pow
from datetime import datetime, timedelta
import json

@pytest.mark.skip # Not implemented
def test_2d_error():
    """
    Id: 1
    Quality requirement: 3.5.2
    Dependencies: This test requires that atleast one method for locating sounds has been implemented.
    Tests: This test collects metrics on the margin of error when locating sounds in two dimensions.
    """
    data = json.loads(open("example_test_data.json").read())
    assert len([d for d in data if within_2d_error(d)]) / len(data) >= 0.8

@pytest.mark.skip # Not implemented
def test_3d_error():
    """
    Id: 2
    Quality requirement: 3.5.4
    Dependencies: This test requires that atleast one method for locating sounds has been implemented. It also requires the system pipeline is implemented in order to correctly measure the delay between data input to data output.
    Tests: This test collects metrics on the total delay from inputted sounds to outputted position.
    """
    data = json.loads(open("example_test_data.json").read())
    assert len([d for d in data if within_3d_error(d)]) / len(data) >= 0.75

@pytest.mark.skip # Not implemented
def test_delay():
    """
    Id: 3
    Quality requirement: 3.5.3
    Dependencies: This test requires that atleast one method for locating sounds has been implemented.
    Tests: This test collects metrics on the margin of error when locating sounds in three dimensions. This in relation to a horizontal x and y plane, as well as a vertical axis z.
    """
    data = json.loads(open("example_test_data.json").read())
    assert len([d for d in data if within_allowed_time(d)]) / len(data) >= 0.8

# Helper functions

def distance(source: tuple[float, float, float], guess: tuple[float, float, float]):
    """
    Checks distance between a source of a sound and a guess.
    """
    return sqrt(pow(source[0] - guess[0], 2) + 
                pow(source[1] - guess[1], 2) + 
                pow(source[2] - guess[2], 2))

def within_2d_error(data):
    """
    Quality requirement: 3.5.2
    Verifies that a guessed postion is within the allowed margin of error for the 2d plane.
    """
    source = data["source"]
    # TODO: guess = guess_pos(data)
    guess = (0, 0, 0) # TODO: temp replace with actual guess above.
    microphone_distance = 100 # TODO: calculate
    source_no_z = (source[0], source[1], 0)
    guess_no_z = (guess[0], guess[1], 0)
    return distance(source_no_z, guess_no_z) <= microphone_distance * 0.2

def within_3d_error(data):
    """
    Quality requirement: 3.5.4
    Verifies that a guessed postion is within the allowed margin of error for three dimensions.
    """
    # TODO: maybe add check that microphones are within the allowed distance of eachother, return true otherwise
    source = data["source"]
    # TODO: guess = guess_pos(data)
    guess = (0, 0, 0) # TODO: temp replace with actual guess above.
    return distance(source, guess) <= 5

def within_allowed_time(data):
    """
    Quality requirement: 3.5.3
    Verifies that a answer is given within the allowed time.
    """
    start = datetime.now()
    # TODO: guess_pos(data) # perform guess
    return datetime.now() - start <= timedelta(seconds=0.5)

if __name__ == "__main__":
    # When collecting metrics this is run instead of the pytest tests.
    data = json.loads(open("example_test_data.json").read())
    
    pass_2d_percentage = len([d for d in data if within_2d_error(d)]) / len(data) * 100
    pass_3d_percentage = len([d for d in data if within_3d_error(d)]) / len(data) * 100
    pass_delay_percentage = len([d for d in data if within_allowed_time(d)]) / len(data) * 100

    print(f"Within 20% of the distance between microphones in a 2d plane, {pass_2d_percentage}% of the time.")
    print(f"Within 5 meters in a 3d space, {pass_3d_percentage}% of the time.")
    print(f"Gives a postion withing 0.5s, {pass_delay_percentage}% of the time.")