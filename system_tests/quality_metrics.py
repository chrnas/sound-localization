"""
This file contains the data collection for quality metrics related to the system.
"""

# TODO: add test id's


def test_2d_error():
    """
    Quality requirement: 3.5.2
    Dependencies: This test requires that atleast one method for locating sounds has been implemented.
    Tests: This test collects metrics on the margin of error when locating sounds in two dimensions.
    """
    pass

def test_3d_error():
    """
    Quality requirement: 3.5.4
    Dependencies: This test requires that atleast one method for locating sounds has been implemented. It also requires the system pipeline is implemented in order to correctly measure the delay between data input to data output.
    Tests: This test collects metrics on the total delay from inputted sounds to outputted position.
    """
    print("hello world")
    pass

def test_delay():
    """
    Quality requirement: 3.5.3
    Dependencies: This test requires that atleast one method for locating sounds has been implemented.
    Tests: This test collects metrics on the margin of error when locating sounds in three dimensions. This in relation to a horizontal x and y plane, as well as a vertical axis z.
    """
    pass