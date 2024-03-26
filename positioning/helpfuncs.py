#import numpy
import math
import copy
import time

class Microphone:

    def __init__(self, distance, coords):
        self.distance = distance
        self.coords = coords
    

def get_error(coords, mics):  
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

def get_middle(mics):
    average_pos = []
    for axis in range(len(mics[0].coords)):
        average = 0
        for mic in mics:
            average += mic.coords[axis]
        average /= len(mics)
        
        average_pos.append(average)

    return average_pos
    

def travel(mics):
    curr_best_pos = True
    no_change = False
    curr_pos = [15, 15, 30]
    while not no_change:
        no_change = True
        for axis in range(len(curr_pos)):
            curr_pos[axis] += 1
            move_positive = get_error(curr_pos, mics)
            curr_pos[axis] -= 2
            move_negative = get_error(curr_pos, mics)
            curr_pos[axis] += 1
            if move_positive == move_negative:
                move_dir = 0
            elif move_positive < move_negative:
                move_dir = 1
            else:
                move_dir = -1
            
            while curr_best_pos:
                next_pos = curr_pos.copy()
                next_pos[axis] += move_dir 
                print("CURR: " + str(curr_pos) + " " + str(get_error(curr_pos, mics)))
                print("NEXT: " + str(next_pos) + " " + str(get_error(next_pos, mics)))
                if get_error(curr_pos, mics) > get_error(next_pos, mics):
                    no_change = False
                    curr_pos = next_pos
                else:
                    curr_best_pos = False

            curr_best_pos = True
    return curr_pos

def travel_lines(mics):
    smallest = [i for i in mics[0].coords]
    biggest = [i for i in mics[0].coords]

    for mic in mics:
        for i in range(len(mic.coords)):
            if(mic.coords[i] < smallest[i]):
                smallest[i] = math.floor(mic.coords[i])
            if(mic.coords[i] > biggest[i]):
                biggest[i] = math.ceil(mic.coords[i])

    for i in biggest:
        i += 1

    

def travel_matrix(mics):
    smallest = [i for i in mics[0].coords]
    biggest = [i for i in mics[0].coords]

    for mic in mics:
        for i in range(len(mic.coords)):
            if(mic.coords[i] < smallest[i]):
                smallest[i] = math.floor(mic.coords[i])
            if(mic.coords[i] > biggest[i]):
                biggest[i] = math.ceil(mic.coords[i])

    best_error = float("inf")
    best_pos = [i for i in mics[0].coords]

    start_time = time.time()
    for x in range(smallest[0], biggest[0] + 1):
        for y in range(smallest[1], biggest[1] + 1):
            for z in range(smallest[2], biggest[2] + 1):
                if best_error > get_error((x, y, z), mics):
                    best_error = get_error((x, y, z), mics)
                    best_pos = [x, y, z]

    print("Loop time: " + str(time.time() - start_time))
    return best_pos 

def get_distance(t1, t2):
    distance = 0
    for i in range(len(t1)):
        distance += (t1[i] - t2[i])**2
    
    return math.sqrt(distance)

if __name__ == "__main__":
    start_time = time.time()
    actual_pos = [15, 15, 15]

    mic_positions = [[0, 0, 30], [0, 30, 0], [30, 30, 0], [30, 0, 0]]
    distances = [get_distance(actual_pos, mic) for mic in mic_positions]
    #for i in range(len(mic_positions))
    first_dist = distances[0]

    for dist in distances:
        dist -= first_dist

    mics = []
    for i in range(len(mic_positions)):
        mic = Microphone(distances[i], mic_positions[i])
        mics.append(mic)

    resultpos = travel_matrix(mics)
    print(resultpos)
    print("Time: " + str(time.time() - start_time))

    print("Accuracy test:")
    """
    for x in range(30):
        for y in range(30):
            print("(" + str(y) + " " + str(round(get_error((x, y, 0), mics), 1)), end = ") ")
        print(x)
    """

