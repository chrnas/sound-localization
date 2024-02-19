"""
This module provides various functions for testing.

Functions:
    * test_add: Performs test on the function add.
"""

import pytest
from my_module import add


def test_add_numbers():
    """
    Test the add_numbers function.

    This function checks if the add_numbers function produces the expected results.
    """
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
    assert add(-1, -1) == -2


if __name__ == "__main__":
    pytest.main()
