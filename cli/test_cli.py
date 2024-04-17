# Run file from parent folder with -m
#import pytest
import subprocess
import json

import Positioning as pos
import ecohandling as eco
from cli import main_loop

## BEHÖVER HJÄLP..

def test_add_mic():
    user_input = 'MicAdd 1 2 3'.encode()
    subprocess.run(["python3", "main.py"], input=user_input, capture_output=True)
    with open("Positioning/microphones.json", "r") as infile:
        file = json.load(infile)
    assert file == [{'name': '1', 'latitude': 2.0, 'longitude': 3.0}]

    
    user_input = 'MicAdd 2 3 4'.encode()
    subprocess.run(["python3", "main.py"], input=user_input, capture_output=True)
    with open("Positioning/microphones.json", "r") as infile:
        file = json.load(infile)
    
    assert file == [{'name': '1', 'latitude': 2.0, 'longitude': 3.0},
                    {'name': '2', 'latitude': 3.0, 'longitude': 4.0}]
    
    

    

def test_pos_list():
    user_input = 'MicList\n'.encode()
    res = subprocess.run(["python3", "main.py"], input=user_input, capture_output=True)
    

    res = res.stdout.decode().split("\n")
    res = res[2:]
    print(res)
    #main_loop.handle_command(["PosList"], pos.pos_methods_data, eco.eco_methods_data)
    

  




















 