"""
This module provides various tools for testing. It is only a demonstration file and not meant to be used.

Functions:
    * TestAddFunciton(numbers): Calculates the average of a list of numbers.
"""
import unittest
from my_module import add 

 """
    Adds two numbers together.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
class TestAddFunction(unittest.TestCase):
    def test_add_positive_numbers(self):
        """
        Test that the `add` function correctly adds positive numbers.
        """
        self.assertEqual(add(2, 3), 5)
