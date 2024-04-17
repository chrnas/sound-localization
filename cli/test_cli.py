# Run file from parent folder with -m
#import pytest
import subprocess
import json
import os

import Positioning as pos
import ecohandling as eco
from cli import main_loop

## BEHÖVER HJÄLP..

def test_add_mic():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../Positioning/microphones.json')
    user_input = 'MicRemove all'.encode()
    subprocess.run(["python3", "main.py"], input=user_input, capture_output=True)

    user_input = 'MicAdd 1 2 3'.encode()
    subprocess.run(["python3", "main.py"], input=user_input, capture_output=True)
    with open(filename, "r") as infile:
        file = json.load(infile)
    assert file == [{'name': '1', 'latitude': 2.0, 'longitude': 3.0}]
 

    """
    user_input = 'MicAdd 2 3 4'.encode()
    subprocess.run(["python3", "main.py"], input=user_input, capture_output=True)
    with open("Positioning/microphones.json", "r") as infile:
        file = json.load(infile)
    
    assert file == [{'name': '1', 'latitude': 2.0, 'longitude': 3.0},
                    {'name': '2', 'latitude': 3.0, 'longitude': 4.0}]
    """
    






















 