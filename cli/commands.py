import json
import os

dirname = os.path.dirname(__file__)


def eco_list(eco_data):
    for method in eco_data:
        print("Method: " + method +
               "  Filename: " + eco_data[method].filename)

def eco_set(eco_data, args):
    """
    EJ FÄRDIG
    """
    print("eco_set: ", eco_data)


def pos_list(pos_data):
    for method in pos_data:
        print("Method: " + method +
               "  Filename: " + pos_data[method].file +
                 "  Active: " + str(pos_data[method].active) +
                   "  Weight: " + str(pos_data[method].weight))



def pos_activate(pos_data, method):
    try:
        pos_data[method[0]].active = True
    except:
        print("Invalid input. Please provide a method name.")
        return

def pos_deactivate(pos_data, method):
    try:
        pos_data[method[0]].active = False
    except:
        print("Invalid input. Please provide a method name.")
        return



def pos_weight(pos_data, args):
    """
    args[0] = method
    args[1] = weight
    """
    try:
        pos_data[args[0]].weight = float(args[1])
    except:
        print("Invalid input. Please provide a method name and a weight.")
        return   


def run_once(pos_data):
    """
    EJ FÄRDIG
    """
    print("run_once: " + pos_data)


def run_cont(pos_data):
    """
    EJ FÄRDIG
    """
    print("run_cont: " + pos_data)


def stop():
    """
    EJ FÄRDIG
    """
    print("STOP")


def mic_list():
    mics = read_mics()
    for mic in mics:
        print(mic)


def mic_add(mic_data):
    mics = read_mics()
    try:
        for mic in mics:
            if mic["name"] == mic_data[0]:
                print("Microphone with that name already exists.")
                return
        new_mic = {
            "name": mic_data[0],
            "latitude": float(mic_data[1]),
            "longitude": float(mic_data[2])
        }
    except:
        print("Invalid input. Please provide a name, longitude and latitude.")
        return
    
    mics.append(new_mic)
    write_mics(mics)
    
    
def mic_remove(mic_data):
    mics = read_mics()

    if mic_data == "all":
        mics = []
    else:
        for mic in mics:
            if mic["name"] == mic_data:
                mics.remove(mic)

    write_mics(mics)


def read_mics():
    with open(os.path.join(dirname, "../positioning/microphones.json"), "r") as file:
        mics = json.load(file)
    return mics


def write_mics(mics):
    with open(os.path.join(dirname, "../positioning/microphones.json"), "w") as file:
        file.write(json.dumps(mics))
