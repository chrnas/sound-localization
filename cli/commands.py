def eco_list(eco_data, params):
    print("Available methods")
    for k in eco_data:
        print("Method: " + k + " Filename: " + eco_data[k].filename)

def eco_set(eco_data):
    print("eco_set: " + eco_data)


def pos_list(pos_data):
    print("pos_list: " + pos_data)


def pos_activate(pos_data):
    print("pos_activate: " + pos_data)


def pos_deactivate(pos_data):
    print("pos_deactivate: " + pos_data)


def pos_weight(pos_data, params):
    print('pow_weight works')


def run_once(pos_data):
    print("run_once: " + pos_data)


def run_cont(pos_data):
    print("run_cont: " + pos_data)


def stop():
    print("STOP")


def mic_list(mic_data):
    print("mic_list: " + mic_data)


def mic_add(mic_data):
    print("mic_add: " + mic_data)


def mic_remove(mic_data):
    print("mic_remove: " + mic_data)
