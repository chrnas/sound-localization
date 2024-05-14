from .methodclass import MethodBaseClass
from typing import Any
from .calcfunctions.receiver import Receiver
from .TidsförskjutningBeräkning import read_wav_file
import numpy as np


class MethodClass(MethodBaseClass):
    def __init__(self) -> None:
        self.settings: dict[str, Any] = {"algorithm": "grid"}
        self.settings["grid settings"] = cf.GridTravelSettings(
            dimensions=2, step=0.1)
        self.settings["number of peaks"] = 5

    def find_source(self, mic_data: dict[Receiver,
                    Union[list[float], str]]) -> list[float]:
        sampling_rate = 1

        for receiver, data in mic_data.items():
            if isinstance(data, str):
                audio_data, sampling_rate = read_wav_file(data)
                mic_data[receiver] = audio_data

    def get_settings(self):
        return self.settings

    def set_setting(self, setting, value):
        if setting in self.settings:
            self.settings[setting] = value


def calculate_amplitudes(self, receivers: dict[Receiver, list[float]],
                         sampling_rate: int = 1) -> list[Receiver]:
    lst = []
    for receiver, samples in receivers.items():
        data = np.sort(np.abs(samples))
        highest_peaks = data[-self.settings["number of peaks"]:]
        lst.append(np.mean(highest_peaks))

        # new_receivers = []
        # for i in range(len(receivers)):

    return lst
