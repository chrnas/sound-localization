import json


def eco_list(eco_data, params):
    """
    EJ FÄRDIG
    """
    print("Available methods")
    for k in eco_data:
        print("Method: " + k + " Filename: " + eco_data[k].filename)

def eco_set(eco_data):
    """
    EJ FÄRDIG
    """
    print("eco_set: " + eco_data)


def pos_list(pos_data):
    """
    FÄRDIG
    """
    for method in pos_data:
        print(method)



def pos_activate(pos_data):
    """
    EJ FÄRDIG
    """
    print("pos_activate: " + pos_data)


def pos_deactivate(pos_data):
    """
    EJ FÄRDIG
    """
    print("pos_deactivate: " + pos_data)


def pos_weight(pos_data, params):
    """
    EJ FÄRDIG
    """
    print('pow_weight works')


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
    """
    FÄRDIG
    """
    with open("Positioning/microphones.json", "r") as infile:
        mics = json.load(infile)
    for mic in mics:
        print(mic)

def mic_add(mic_data):
    """
    FÄRDIG
    """
    with open("Positioning/microphones.json", "r") as infile:
        mics = json.load(infile)

    try:
        for mic in mics:
            if mic["name"] == mic_data[0]:
                print("Microphone with that name already exists.")
                return
        new_mic = {
            "name": mic_data[0],
            "longitude": float(mic_data[1]),
            "latitude": float(mic_data[2])
        }
    except:
        print("Invalid input. Please provide a name, longitude and latitude.")
        return
    
    mics.append(new_mic)
    updated_mics = json.dumps(mics)
    with open("Positioning/microphones.json", "w") as outfile:
        outfile.write(updated_mics)
    


def mic_remove(mic_data):
    """
    FÄRDIG
    """
    with open("Positioning/microphones.json", "r") as infile:
        mics = json.load(infile)

    if mic_data == "all":
        mics = []
    else:
        for mic in mics:
            if mic["name"] == mic_data:
                mics.remove(mic)

    updated_mics = json.dumps(mics)
    with open("Positioning/microphones.json", "w") as outfile:
        outfile.write(updated_mics)

