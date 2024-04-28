from .methodclass import MethodBaseClass
from typing import Any
from .calcfunctions.receiver import Receiver
from .calcfunctions.trilateration import MicrophoneArray
from .calcfunctions.gridtrilaterate import GridTravelSettings, trilaterate_grid
import numpy as np
# from .TidsförskjutningBeräkning import # here I need to get a function that will be able to calculate the time difference between two sample lists. This should be done in two parts creating the wav objects and then calculating the time difference with the internal functions. However, I would like to compress this into a signal function internally


class MethodClass(MethodBaseClass):
    def __init__(self) -> None:
        self.settings: dict[str, Any] = {"algorithm": "gradient"}
        self.settings["grid settings"] = GridTravelSettings(
            dimensions=2, step=0.5)

    def find_source(self, mic_data: list[dict[Receiver, list[float]]]) -> list[float]:

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
        

        def identify_first_sound(sounds):
            """
            Identify the first sound file based on cross-correlation time differences.
            The one with the largest negative time difference when compared to others is the first.

            Args:
                sounds (list of list of float): A list where each item is a sound sample list.

            Returns:
                int: Index of the first sound sample list detected.
            """
            min_time_difference = float('inf')
            first_index = 0

            # Choose one sound as a reference, compare it against all others
            reference_sound = sounds[0]

            for i in range(1, len(sounds)):
                time_difference = calculate_time_difference(reference_sound, sounds[i])
                # If this sound starts before the current reference
                if time_difference < min_time_difference:
                    min_time_difference = time_difference
                    first_index = i

            # Adjust for the fact that the first sound might not be the reference
            if min_time_difference > 0:
                first_index = 0

            return first_index

    def get_settings(self):
        return self.settings

    def set_setting(self, setting, value):
        if setting in self.settings:
            self.settings[setting] = value

    