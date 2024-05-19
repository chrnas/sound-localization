from .methodclass import MethodBaseClass
from typing import Any
from . import calcfunctions
from .cross_correlation import read_wav_file
import numpy as np
from typing import Union


class ADMethod(MethodBaseClass):
    def __init__(self) -> None:
        self.settings: dict[str, Any] = {
            "algorithm": "grid",
            "grid settings": calcfunctions.GridTravelSettings(dimensions=2, step=0.5),
            "number of peaks": 5
        }
        self.all_possible_settings = {
            "algorithm": ["grid"],
            "grid_settings.dimensions": [float],
            "grid_settings.step": [float],
            "grid_settings.smallest_start": [float],
            "grid_settings.biggest_start": [float],
            "grid_settings.smallest_expansion": [float],
            "grid_settings.biggest_expansion": [float],
            "number of peaks": [int]
        }

    def find_source(self, mic_data: dict[calcfunctions.Receiver, Union[list[float], str]]) -> list[float]:
        sampling_rate = 1

        for receiver, data in mic_data.items():
            if isinstance(data, str):
                audio_data, sampling_rate = read_wav_file(data)
                mic_data[receiver] = audio_data

        receivers = self.calculate_amplitudes(mic_data, sampling_rate)

        position = calcfunctions.trilaterate_grid(
            receivers, self.settings["grid settings"])

        return position

    def get_settings(self):
        return self.settings

    def set_setting(self, setting: str, value: Union[str, int, float, list[int]]) -> None:
        if setting.startswith('grid_settings.'):
            grid_setting = setting.split('.', 1)[1]
            if hasattr(self.settings['grid settings'], grid_setting):
                expected_type = self.all_possible_settings[f'grid_settings.{
                    grid_setting}'][0]
                if not isinstance(value, expected_type):
                    try:
                        value = expected_type(value)
                    except (ValueError, TypeError):
                        raise ValueError(f"Invalid type for setting {setting}. Expected {
                                         expected_type.__name__}, but got {type(value).__name__}")
                setattr(self.settings['grid settings'], grid_setting, value)
            else:
                raise ValueError(
                    f"No grid setting by the name of {grid_setting}")
        elif setting in self.all_possible_settings:
            expected_values = self.all_possible_settings[setting]
            if expected_values and not isinstance(expected_values[0], type):
                if value not in expected_values:
                    raise ValueError(f"Invalid value for setting {setting}. Expected one of {
                                     expected_values}, but got {value}")
            else:
                expected_type = expected_values[0]
                if not isinstance(value, expected_type):
                    try:
                        value = expected_type(value)
                    except (ValueError, TypeError):
                        raise ValueError(f"Invalid type for setting {setting}. Expected {
                                         expected_type.__name__}, but got {type(value).__name__}")
            self.settings[setting] = value
        else:
            raise ValueError(f"No setting by the name of {setting}")

    def calculate_amplitudes(self, receivers: dict[calcfunctions.Receiver, list[float]], sampling_rate: int = 1) -> list[calcfunctions.Receiver]:
        new_receivers = []
        for receiver, samples in receivers.items():
            data = np.sort(np.abs(samples))
            highest_peaks = data[-self.settings["number of peaks"]:]
            receiver.set_distance_difference(np.mean(highest_peaks))
            new_receivers.append(receiver)

        return new_receivers
