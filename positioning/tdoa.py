from .methodclass import MethodBaseClass
from typing import Any
from .calcfunctions.receiver import Receiver
from .calcfunctions.trilateration import MicrophoneArray
from .calcfunctions.gridtrilaterate import GridTravelSettings, trilaterate_grid
from .TidsförskjutningBeräkning import identify_first_sound, calc_offset_from_samples, read_wav_file
import numpy as np
from itertools import combinations
from typing import Union


class MethodClass(MethodBaseClass):
    def __init__(self) -> None:
        self.settings: dict[str, Any] = {"algorithm": "grid"}
        self.settings["grid settings"] = GridTravelSettings(
            dimensions=2, step=0.1)

    def find_source(self, mic_data: dict[Receiver, Union[list[float], str]]) -> list[float]:

        sampling_rate = 1

        for receiver, data in mic_data.items():
            if isinstance(data, str):
                audio_data, sampling_rate = read_wav_file(data)
                mic_data[receiver] = audio_data

        receivers: list[Receiver] = calculate_time_differences(
            mic_data, sampling_rate=sampling_rate)

        if self.settings['algorithm'] == "grid":
            dimenstion: int = len(receivers[0].get_position())
            self.settings["grid settings"].set_dimension(dimension=dimenstion)
            position = trilaterate_grid(
                mics=receivers, settings=self.settings["grid settings"])
            return position

        elif self.settings['algorithm'] == "gradient":
            array: MicrophoneArray = MicrophoneArray(receivers)
            position, _ = array.estimate_position()
            return position.tolist()
        else:
            return [404, 404, 404]

    def get_settings(self):
        return self.settings

    def set_setting(self, setting, value):
        if setting in self.settings:
            self.settings[setting] = value


def calculate_time_differences(receivers: dict[Receiver, list[float]], sampling_rate: int = 1) -> list[Receiver]:
    """
    Calculates and sets the time differences for all receivers relative to the first detected receiver by averaging
    all possible paths of time differences.

    Args:
        receivers (dict): Dictionary where keys are Receiver instances and values are lists of sound samples.
        sampling_rate (int): The sampling rate of the audio data.

    Returns:
        list: List of updated Receiver objects with set time differences.
    """
    # Identify the first detected sound
    sounds = [samples for _, samples in receivers.items()]
    first_sound_index = identify_first_sound(sounds)
    first_receiver = list(receivers.keys())[first_sound_index]

    # Calculate all pairwise time differences
    pairwise_time_diffs = {}
    for (r1, samples1), (r2, samples2) in combinations(receivers.items(), 2):
        time_diff = calc_offset_from_samples(
            samples2, samples1, rate1=sampling_rate, rate2=sampling_rate)
        pairwise_time_diffs[(r1, r2)] = time_diff
        pairwise_time_diffs[(r2, r1)] = -time_diff

    # Set the time difference for the first receiver to zero
    first_receiver.set_time_difference(0.0)

    # Calculate time differences relative to the first receiver using all possible paths
    for receiver in receivers:
        if receiver != first_receiver:
            all_paths = find_all_paths(
                first_receiver, receiver, receivers, pairwise_time_diffs)
            if all_paths:
                # Average time differences from all valid paths
                average_time_diff = np.mean(
                    [sum(pairwise_time_diffs[step] for step in path) for path in all_paths])
                receiver.set_time_difference(average_time_diff)

    ordered_microphones = list(receivers.keys())
    ordered_microphones.sort(
        key=lambda mic: mic.get_time_difference())

    return ordered_microphones


def find_all_paths(start, end, receivers, pairwise_time_diffs):
    """
    Finds all paths from start to end using a depth-first search approach.

    Args:
        start (Receiver): Starting receiver.
        end (Receiver): Ending receiver.
        receivers (dict): Dictionary of receivers.
        pairwise_time_diffs (dict): Dictionary of pairwise time differences.

    Returns:
        list: List of paths, where each path is a list of tuples indicating the pairwise steps.
    """
    def dfs(current, end, path):
        if current == end:
            return [path]
        paths = []
        for next_receiver in receivers:
            if (current, next_receiver) in pairwise_time_diffs and next_receiver not in [p[1] for p in path]:
                new_path = path + [(current, next_receiver)]
                paths.extend(dfs(next_receiver, end, new_path))
        return paths

    return dfs(start, end, [])


def set_time_differences(receivers_time_diffs: dict[Receiver, float]) -> list[Receiver]:
    """
    Sets the time differences for each receiver based on a dictionary mapping and returns the list of receivers.

    Args:
        receivers_time_diffs (dict): A dictionary where keys are Receiver instances and values are time differences.

    Returns:
        list: A list of the updated Receiver objects.
    """
    # List to hold the receivers after updating
    updated_receivers = []

    for receiver, time_diff in receivers_time_diffs.items():
        receiver.set_time_difference(time_diff)
        updated_receivers.append(receiver)

    return updated_receivers
