# Run file from parent folder with -m
import pytest
import subprocess

import Positioning  as pos
import ecohandling as eco
from cli import main_loop

## BEHÖVER HJÄLP..

def test_pos_list(monkeypatch, capfd):

    main_loop.handle_command(["PosList"], pos.pos_methods_data, eco.eco_methods_data)
    

  




















 