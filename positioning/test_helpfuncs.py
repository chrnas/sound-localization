import pytest
import helpfuncs

def create_mics(actual_pos, mic_positions):
    distances = [helpfuncs.get_distance(actual_pos, mic) for mic in mic_positions]
    first_dist = distances[0]
    for dist in distances:
        dist -= first_dist
    mics = []
    for i in range(len(mic_positions)):
        mic = helpfuncs.Microphone(distances[i], mic_positions[i])
        mics.append(mic)
    return mics


def test_2d_middle():
    actual_pos = [15, 15, 0]
    mic_positions = [[0, 0, 0], [0, 30, 0], [30, 30, 0], [30, 0, 0]]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = helpfuncs.travel(mics)
    assert resultpos == actual_pos

def test_2d_corner1():
    actual_pos = [0, 0, 0]
    mic_positions = [[0, 0, 0], [0, 30, 0], [30, 30, 0], [30, 0, 0]]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = helpfuncs.travel(mics)
    assert resultpos == actual_pos

def test_2d_corner2():
    actual_pos = [0, 30, 0]
    mic_positions = [[0, 0, 0], [0, 30, 0], [30, 30, 0], [30, 0, 0]]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = helpfuncs.travel(mics)
    assert resultpos == actual_pos

def test_2d_corner3():
    actual_pos = [30, 30, 0]
    mic_positions = [[0, 0, 0], [0, 30, 0], [30, 30, 0], [30, 0, 0]]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = helpfuncs.travel(mics)
    assert resultpos == actual_pos

def test_2d_corner4():
    actual_pos = [30, 0, 0]
    mic_positions = [[0, 0, 0], [0, 30, 0], [30, 30, 0], [30, 0, 0]]
    mics = create_mics(actual_pos, mic_positions)
    resultpos = helpfuncs.travel(mics)
    assert resultpos == actual_pos


