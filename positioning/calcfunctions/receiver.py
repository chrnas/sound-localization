from . import constants
import numpy as np


class Receiver:

    def __init__(self, coords):
        self.distance_difference = 0
        if isinstance(coords, np.ndarray) or isinstance(coords, list):
            self.coords = coords
        else:
            raise ValueError

    def get_distance_difference(self):
        return self.distance_difference

    def get_time_difference(self):
        return self.distance_difference/constants.SOUNDSPEED

    def set_distance_difference(self, distance_difference):
        self.distance_difference = distance_difference

    def set_time_difference(self, time_difference):
        self.distance_difference = time_difference * constants.SOUNDSPEED

    def get_position(self):
        return self.coords

    def create_mics(positions):
        mics = [Receiver(position) for position in positions]
        return mics
    
    def __str__(self):
        return f"Receiver at position {self.coords} with time difference {self.get_time_difference():.3f}s"

