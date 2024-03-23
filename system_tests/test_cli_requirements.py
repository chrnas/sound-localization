"""
This file contains tests related to the requirements on the CLI.
"""

# TODO: replace ... is not None with bool(...)
# TODO: add command arguments as test input instead to make more dynamic
# TODO: add checks for error handling
# TODO: add test dependencies

import subprocess
import pytest
import re

@pytest.mark.skip # Not implemented
def test_developed_cli():
    """
    Id: 4
    CLI requirement: 3.3.1
    Tests: That a CLI has been implemented to some level (it has atleast one command).
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args)
    assert p.returncode == 0

@pytest.mark.skip # Not implemented
def test_gives_coordinate():
    """
    Id: 5
    CLI requirement: 3.3.2
    Tests: That the CLI gives coordinate for a located sound in the form of longitude and latitude.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # Example pass: Possible location -777.777, 888.0
    # Example fail: Possible location -777.777 888.0
    # Example fail: Possible location -777., 888.0
    assert re.fullmatch(r"Possible location -?\d+\.\d+, -?\d+\.\d+", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_error_margin():
    """
    Id: 6
    CLI requirement: 3.3.3
    Tests: That the CLI gives a margin of error after together with the location of the sound.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # Example pass: Margin of error: 123.123 meters
    # Example pass: Margin of error: 1.0 meter
    # Example fail: Margin of error: 123.123 meter
    # Example fail: Margin of error: 1.0 meters
    assert re.fullmatch(r"Margin of error: (1\.0+ meter|(?!1\.0+)\d+\.\d+ meters)", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_choose_method():
    """
    Id: 7
    CLI requirement: 3.3.4
    Tests: That the user can choose between using different types of positioning methods.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # Assuming no other methods for locating sounds has been added.
    # Example pass: Now using method TDOA to locate sounds
    # Example pass: Now using method AD to locate sounds
    # Example fail: Now using 
    assert re.fullmatch(r"Now using method (TDOA|AD) to locate sounds", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_add_method():
    """
    Id: 8
    CLI requirement: 3.3.5
    Tests: That a user can add new postioning methods without access to the source code.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # Example pass: Added method AAA for locating sounds
    # Example fail: Added method A A for locating sounds
    assert re.fullmatch(r"Added method \S+ for locating sounds", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_add_microphones():
    """
    Id: 9
    CLI requirement: 3.3.6
    Tests: That the user can configure which microphones are used.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # Example pass: Added microphone AAA at -888.0, 777.777, 555.0
    # Example pass: Added microphone BBB at -888.0, 777.777
    # Example fail: Added microphone CCC at -888.0, 777.777 555.0
    assert re.fullmatch(r"Added microphone \S+ at -?\d+\.\d+, -?\d+\.\d+(, -?\d+\.\d+)?", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_remove_microphones():
    """
    Id: 10
    CLI requirement: 3.3.6
    Tests: That the user can configure which microphones are used.
    """
    # TODO: maybe have to add microphone before.
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # Example pass: Removed microphone AAA
    # Example fail: Removed microphone B B
    assert re.fullmatch(r"Removed microphone \S+", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_choose_echohandling():
    """
    Id: 11
    CLI requirement: 3.3.7
    Tests: That the user can choose between different methods for handling of echo.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # Example pass: Now using AAA to handle echos
    # Example fail: Now using AAA to handle ecos
    assert re.fullmatch(r"Now using \S+ to handle echos", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_add_echohandling():
    """
    Id: 12
    CLI requirement: 3.3.8
    Tests: That the user can add methods for handling of echo without access to the source code.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # Example pass: Added method AAA for handling echos
    # Example fail: Added method AAA for handling ecos
    assert re.fullmatch(r"Added method \S+ for handling echos", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_combine_methods():
    """
    Id: 13
    CLI requirement: 3.3.9
    Tests: That the user can choose to use multiple methods for positioning to get a weighted average.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # NOTE: missing s after method not caught
    # Example pass: Now using method AAA to locate sounds
    # Example pass: Now using method AAA and BBB together to locate sounds
    # Example pass: Now using methods AAA, BBB and CCC together to locate sounds
    # Example fail: Now using methods AAA, and BBB together to locate sounds
    # Example fail: Now using method AAA together to locate sounds
    assert re.fullmatch(r"Now using methods? \S+((, \S+)? and \S+ together)? to locate sounds", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_weigh_methods():
    """
    Id: 14
    CLI requirement: 3.3.9
    Tests: That the user can set the weight of a method when using multiple methods together.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # Example pass: Set method AAA's weight to 1.1
    # Example pass: Set method SSS' weight to 2.2
    # Example fail: Set method AAA' weight to 1.1
    # Example fail: Set method SSS's weight to 2.2
    assert re.fullmatch(r"Set method \S+([sS]'|[^sS]'s) weight to \d+\.\d+", p.stdout.decode()) is not None