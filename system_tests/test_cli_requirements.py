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
    assert re.match(r"Now using (TDOA|AD) to locate sounds", p.stdout.decode()) is not None

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
def test_configure_microphones():
    """
    Id: 9
    CLI requirement: 3.3.6
    Tests: That the user can configure which microphones are used.
    """
    pass

@pytest.mark.skip # Not implemented
def test_choose_ecohandling():
    """
    Id: 10
    CLI requirement: 3.3.7
    Tests: That the user can choose between different methods for handling of eco.
    """
    pass

@pytest.mark.skip # Not implemented
def test_add_ecohandling():
    """
    Id: 11
    CLI requirement: 3.3.8
    Tests: That the user can add methods for handling of eco without access to the source code.
    """
    pass

@pytest.mark.skip # Not implemented
def test_combine_methods():
    """
    Id: 12
    CLI requirement: 3.3.9
    Tests: That the user can choose to use multiple methods for positioning to get a weighted average.
    """
    pass