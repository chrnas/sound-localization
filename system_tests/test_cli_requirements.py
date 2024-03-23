"""
This file contains tests related to the requirements on the CLI.
"""

import subprocess
import pytest
import re

@pytest.mark.skip # Not implemented
def test_developed_cli():
    """
    Id: 4
    CLI requirement: 3.3.1
    Tests: That a CLI has been implemented to some level.
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
    assert re.match(r"Possible location -?\d+\.\d+, -?\d+\.\d+", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_error_margin():
    """
    Id: 6
    CLI requirement: 3.3.3
    Tests: That the CLI gives a margin of error after together with the location of the sound.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    assert re.match(r"Margin of error: \d+\.\d+ meters", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_choose_method():
    """
    Id: 7
    CLI requirement: 3.3.4
    Tests: That the user can choose between using different types of positioning methods.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    assert re.match(r"Now using method (TDOA|AD) to locate sounds", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_add_method():
    """
    Id: 8
    CLI requirement: 3.3.5
    Tests: That a user can add new postioning methods without access to the source code.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # TODO: maybe add second test which checks only methods with names without space can be added.
    assert re.match(r"Added method \S+ for locating sounds", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_add_microphones():
    """
    Id: 9.1
    CLI requirement: 3.3.6
    Tests: That the user can configure which microphones are used.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # TODO: maybe add second test which checks only methods with names without space can be added.
    assert re.match(r"Added microphone \S+ at -?\d+\.\d+, -?\d+\.\d+(, -?\d+\.\d+)?", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_remove_microphones():
    """
    Id: 9.2
    CLI requirement: 3.3.6
    Tests: That the user can configure which microphones are used.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # TODO: maybe add second test which checks only methods with names without space can be added.
    assert re.match(r"Removed microphone \S+", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_choose_echohandling():
    """
    Id: 10
    CLI requirement: 3.3.7
    Tests: That the user can choose between different methods for handling of echo.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # TODO: maybe add second test which checks only methods with names without space can be added.
    assert re.match(r"Now using \S+ to handle echos", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_add_echohandling():
    """
    Id: 11
    CLI requirement: 3.3.8
    Tests: That the user can add methods for handling of echo without access to the source code.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # TODO: maybe add second test which checks only methods with names without space can be added.
    assert re.match(r"Added method \S+ for handling echos", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_combine_methods():
    """
    Id: 12.1
    CLI requirement: 3.3.9
    Tests: That the user can choose to use multiple methods for positioning to get a weighted average.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # TODO: maybe add second test which checks only methods with names without space can be added.
    assert re.match(r"Now using methods? \S+((, \S+)? and \S+ together)? to locate sounds", p.stdout.decode()) is not None

@pytest.mark.skip # Not implemented
def test_weigh_methods():
    """
    Id: 12.1
    CLI requirement: 3.3.9
    Tests: That the user can set the weight of a method when using multiple methods together.
    """
    args = [] # TODO: provide run arguments
    p = subprocess.run(args, capture_output=True)
    # TODO: maybe add second test which checks only methods with names without space can be added.
    assert re.match(r"Set method \S+([sS]'|[^sS]'s) weight to \d+\.\d+", p.stdout.decode()) is not None