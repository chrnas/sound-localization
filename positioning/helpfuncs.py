#import numpy
import math
import copy
import time

class Microphone:

    def __init__(self, distance, coords):
        self.distance = distance
        self.coords = coords


class TravelSettings():

    def __init__(self, dimensions, step):
        self.dimensions = dimensions #Number of dimensions the settings are for
        self.smallest_start = [0 for i in range(dimensions)] #Smallest coordinates to always include
        self.biggest_start = [0 for i in range(dimensions)] #Biggest coordinates to always include
        self.smallest_expansion = [1 for i in range(dimensions)] #How far outside mic area to search in negative coords
        self.biggest_expansion = [1 for i in range(dimensions)] #How far outside mic area to search in positive coords
        self.step = step #How far to travel between each search point
    

def get_error(coords, mics):
    """
    Calculate an error heuristic for a given position in the grid. 
    See the arcitecture document for an explanation of the error heuristic.

    @param list coords: The coordinates to calculate the error for
    @params list mics: Instances of the Microphone class
    @return float: The error of the given position
    """  
    previous_mic = mics[-1]
    error = 0
    for mic in mics:
        current_eqv = 0
        previous_eqv = 0
        for i in range(len(coords)):
            current_eqv += (coords[i] - mic.coords[i])**2
            previous_eqv += (coords[i] - previous_mic.coords[i])**2

        left_side = math.sqrt(current_eqv) - math.sqrt(previous_eqv)

        right_side = mic.distance - previous_mic.distance
        
        error += abs(left_side - right_side)
    
    return error
    

def travel_grid(mics, smallest, biggest, step):
    """
    Scan the grid and return the best position of the sound source
    Gets called on by find_sound_source

    @param list mics: Instances of the Microphone class
    @param list smallest: The smallest coordinates to search in
    @param list biggest: The biggest coordinates to search in
    @param step: The step size to travel in each direction
    @return list: Guess of the sound source position
    """

    best_error = float("inf")
    best_pos = [i for i in mics[0].coords]
    positions = [i for i in smallest]

    last_changed = False
    
    while True:
        current_error = get_error(positions, mics)
        if best_error > current_error:
            best_pos = positions.copy()
            best_error = current_error

        for i in range(len(positions)):
            positions[i] += step
            if positions[i] > biggest[i]:
                positions[i] = smallest[i]
            else:
                break

        if not last_changed and smallest[-1] != positions[-1]:
            last_changed = True
        elif last_changed and positions[-1] == smallest[-1]:
            break
        
    return best_pos


def find_sound_source(mics, settings):
    """
    Sets parameters for the grid search and calls the travel_grid function to 
    find the best position of the sound source

    @param list mics: Instances of the Microphone class
    @param TravelSettings settings: The settings for the search
    @return list: Guess of the sound source position
    """
    smallest = [settings.smallest_start[i] for i in range(settings.dimensions)]
    biggest = [settings.biggest_start[i] for i in range(settings.dimensions)]

    for mic in mics:
        for i in range(len(mic.coords)):
            if(mic.coords[i] < smallest[i]):
                smallest[i] = mic.coords[i]
            if(mic.coords[i] > biggest[i]):
                biggest[i] = mic.coords[i]

    for i in range(len(settings.smallest_expansion)):
        smallest[i] -= settings.smallest_expansion[i]
        biggest[i] += settings.biggest_expansion[i]

    best_pos = travel_grid(mics, smallest, biggest, settings.step)
    return best_pos 


def get_distance(sound_pos, mic_pos):
    distance = 0
    for i in range(len(sound_pos)):
        distance += (sound_pos[i] - mic_pos[i])**2
    
    return math.sqrt(distance)


if __name__ == "__main__":
    number_of_mics = input("Please enter the number of microphones: ")
    mic_positions = []
    for i in range(int(number_of_mics)):
        string = input(f"Please enter the coordinates of microphone {i+1}: ")
        coords = [float(num) for num in string.split(" ")]
        mic_positions.append(coords)

    step = float(input("Please enter the accuracy: "))
    settings = TravelSettings(len(mic_positions[0]), step)

    expansion = input("Enter negative search expansion (Default is 1): ")
    settings.smallest_expansion = [expansion for i in settings.smallest_expansion]

    expansion = input("Enter positive search expansion (Default is 1): ")
    settings.biggest_expansion = [expansion for i in settings.biggest_expansion]

    string_actual = input("Please enter the coordinates of the actual position: ")
    actual_pos = [float(num) for num in string_actual.split(" ")]

    
    start_time = time.time()
    
    distances = [get_distance(actual_pos, mic) for mic in mic_positions]
    first_dist = distances[0]
    for dist in distances:
        dist -= first_dist
    print(distances)

    mics = []
    for i in range(int(number_of_mics)):
        mic = Microphone(distances[i], mic_positions[i])
        mics.append(mic)

    resultpos = find_sound_source(mics, settings)
    print(resultpos)
    print("Time: " + str(time.time() - start_time))
