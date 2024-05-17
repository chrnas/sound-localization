from .methodclass import MethodBaseClass
from typing import Any
from . import calcfunctions
from .TidsförskjutningBeräkning import read_wav_file
import numpy as np


class MethodClass(MethodBaseClass):
    def __init__(self) -> None:
        self.settings: dict[str, Any] = {"algorithm": "grid"}
        self.settings["grid settings"] = calcfunctions.GridTravelSettings(
            dimensions=2, step=0.5)
        self.settings["number of peaks"] = 5

    def find_source(self, mic_data: dict[calcfunctions.Receiver,
                    Union[list[float], str]]) -> list[float]:
        sampling_rate = 1

        for receiver, data in mic_data.items():
            if isinstance(data, str):
                audio_data, sampling_rate = read_wav_file(data)
                mic_data[receiver] = audio_data

        recievers = calculate_amplitudes(mic_data, sampling_rate)

        position = calcfunctions.trilaterate_grid(recievers, self.settings["grid settings"])

        return position

    def get_settings(self):
        return self.settings

    def set_setting(self, setting, value):
        if setting in self.settings:
            self.settings[setting] = value


def calculate_amplitudes(self, receivers: dict[calcfunctions.Receiver, list[float]],
                         sampling_rate: int = 1) -> list[calcfunctions.Receiver]:
    new_recievers = []
    for receiver, samples in receivers.items():
        data = np.sort(np.abs(samples))
        highest_peaks = data[-self.settings["number of peaks"]:]
        receiver.set_distance_difference(np.mean(highest_peaks))
        new_recievers.append(receiver)

    return new_recievers
