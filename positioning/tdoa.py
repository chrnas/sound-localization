from .methodclass import MethodBaseClass
from typing import Any
from .calcfunctions.receiver import Receiver
from .calcfunctions.trilateration import MicrophoneArray
from .calcfunctions.gridtrilaterate import GridTravelSettings, trilaterate_grid
import numpy as np


class MethodClass(MethodBaseClass):
    def __init__(self) -> None:
        self.settings: dict[str, Any] = {"algorithm": "gradient"}
        self.settings["grid settings"] = GridTravelSettings(
            dimensions=2, step=0.5)

    def find_source(self, mic_data: list[Receiver]) -> list[float]:

        if self.settings['algorithm'] == "grid":
            dimenstion: int = len(mic_data[0].get_position())
            self.settings["grid settings"].set_dimension(dimension=dimenstion)
            position = trilaterate_grid(
                mics=mic_data, settings=self.settings["grid settings"])
            return position

        elif self.settings['algorithm'] == "gradient":
            array: MicrophoneArray = MicrophoneArray(mic_data)
            position, _ = array.estimate_position()
            return position.tolist()

    def get_settings(self):
        return self.settings

    def set_setting(self, setting, value):
        if setting in self.settings:
            self.settings[setting] = value

