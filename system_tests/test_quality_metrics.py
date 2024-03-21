"""
This file contains the data collection for quality metrics related to the system.
"""

# TODO: add test id's
# TODO: This file assumes output is given in meters

import pytest
from math import sqrt, pow
from datetime import datetime, timedelta
import json

@pytest.mark.skip # Not implemented
def test_2d_error():
    """
    Quality requirement: 3.5.2
    Dependencies: This test requires that atleast one method for locating sounds has been implemented.
    Tests: This test collects metrics on the margin of error when locating sounds in two dimensions.
    """
    pass

@pytest.mark.skip # Not implemented
def test_3d_error():
    """
    Quality requirement: 3.5.4
    Dependencies: This test requires that atleast one method for locating sounds has been implemented. It also requires the system pipeline is implemented in order to correctly measure the delay between data input to data output.
    Tests: This test collects metrics on the total delay from inputted sounds to outputted position.
    """
    print("hello world")
    pass

@pytest.mark.skip # Not implemented
def test_delay():
    """
    Quality requirement: 3.5.3
    Dependencies: This test requires that atleast one method for locating sounds has been implemented.
    Tests: This test collects metrics on the margin of error when locating sounds in three dimensions. This in relation to a horizontal x and y plane, as well as a vertical axis z.
    """
    pass

# Helper functions

def distance(source: tuple[float, float, float], guess: tuple[float, float, float]):
    """
    Checks distance between a source of a sound and a guess.
    """
    return sqrt(pow(source[0] - guess[0], 2), 
                pow(source[1] - guess[1], 2), 
                pow(source[2] - guess[2], 2))

def within_2d_error(microphone_distance: float, source: tuple[float, float, float], guess: tuple[float, float, float]):
    """
    Quality requirement: 3.5.2
    Verifies that a guessed postion is within the allowed margin of error for the 2d plane.
    """
    source_no_z = (source[0], source[1], 0) # TODO: assumes (x, y, z)
    guess_no_z = (guess[0], guess[1], 0) # TODO: assumes (x, y, z)
    return distance(source_no_z, guess_no_z) <= microphone_distance * 0.2

def within_3d_error(source: tuple[float, float, float], guess: tuple[float, float, float]):
    """
    Quality requirement: 3.5.4
    Verifies that a guessed postion is within the allowed margin of error for three dimensions.
    """
    # TODO: maybe add check that microphones are within the allowed distance of eachother, return true otherwise
    return distance(source, guess) <= 5

def within_allowed_time(data):
    """
    Quality requirement: 3.5.3
    Verifies that a answer is given within the allowed time.
    """
    start = datetime.now()
    # TODO: guess(data) # perform guess
    return datetime.now() - start <= timedelta(seconds=0.5)

if __name__ == "__main__":
    # When collecting metrics this is run instead of the pytest tests.
    pass