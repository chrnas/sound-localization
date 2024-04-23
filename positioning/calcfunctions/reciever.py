import constants

class Microphone:

    def __init__(self, coords: list[float, float]):
        self.distance_difference = 0
        self.coords = coords

    def get_distance_difference(self):
        return self.distance_difference
    
    def get_time_difference(self):
        return self.distance_difference/constants.SOUNDSPEED
    
    def set_distance_difference(self, distance_difference):
        self.distance_difference = distance_difference

    def set_time_difference(self, time_difference):
        self.distance_difference = time_difference * constants.SOUNDSPEED

    def get_positions(self):
        return self.coords

def create_mics(positions):
    mics = [Microphone(position for position in positions )]

    return mics