import json
import os
import time
import threading
from positioning.calcfunctions import Receiver
from positioning.positioning_handler import PosMethodData
import itertools

from typing import Union, Optional

# Define directories
dirname = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'positioning'))
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def pos_list(positioning_methods: dict[str, PosMethodData]) -> None:
    for method_name, method_data in positioning_methods.items():
        print(f"Method: {method_name}  Filename: {method_data.file}")


def pos_set_setting(positioning_methods: dict[str, PosMethodData], method_name: str, setting_name: str, setting_value: Union[str, int, float, dict]) -> None:
    """
    Apply a specific setting to a specific positioning method.
    """
    try:
        positioning_methods[method_name].method.set_setting(
            setting=setting_name, value=setting_value)
        print(
            f"Setting {setting_name} for {method_name} updated to: {setting_value}")
    except Exception as e:
        print(f"Invalid input. Exited with error: {e}")


def calculate_position(positioning_methods: dict[str, PosMethodData], method_key: str) -> None:
    """
    Calculate the position using the specified positioning method and microphone data.
    """
    def spinner():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            print('\rCalculating position ' + c, end='', flush=True)
            time.sleep(0.1)

    mic_data = read_mics()

    if method_key not in positioning_methods:
        print(f"Method {method_key} not found in positioning_methods.")
        return

    method = positioning_methods[method_key]

    mic_data_dict: dict[Receiver, Union[str, list[float]]] = {}
    for mic in mic_data:
        receiver = Receiver([mic['latitude'], mic['longitude']])
        soundfile_path = os.path.join(
            base_path, mic['soundfile']) if 'soundfile' in mic else []
        mic_data_dict[receiver] = soundfile_path

    done = False
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    try:
        position = method.method.find_source(mic_data_dict)
        done = True
        spinner_thread.join()
        print(f"\nCalculated position using {method_key}: {position}")
    except Exception as e:
        done = True
        spinner_thread.join()
        print(f"\nError calculating position: {e}")


def mic_list() -> None:
    mics = read_mics()
    for mic in mics:
        soundfile_info = ", Soundfile: {mic['soundfile']}" if 'soundfile' in mic else ""
        print(
            f"Name: {mic['name']}, Latitude: {mic['latitude']}, Longitude: {mic['longitude']}{soundfile_info}")


def mic_add(mic_data: list[str], soundfile: Optional[str] = None) -> None:
    mics = read_mics()
    try:
        for mic in mics:
            if mic["name"] == mic_data[0]:
                print("Microphone with that name already exists.")
                return
        new_mic = {
            "name": mic_data[0],
            "latitude": float(mic_data[1]),
            "longitude": float(mic_data[2]),
        }
        if soundfile:
            new_mic["soundfile"] = os.path.relpath(soundfile, base_path)
    except Exception as e:
        print(f"Invalid input. Exited with error code: {e}")
        return

    mics.append(new_mic)
    write_mics(mics)


def mic_remove(mic_name: str) -> None:
    mics = read_mics()
    if mic_name == "all":
        mics = []
    else:
        for mic in mics:
            if mic["name"] == mic_name:
                mics.remove(mic)
    write_mics(mics)


def mic_add_soundfile(mic_name: str, soundfile: str) -> None:
    mics = read_mics()
    for mic in mics:
        if mic["name"] == mic_name:
            mic["soundfile"] = os.path.relpath(soundfile, base_path)
            write_mics(mics)
            print(f"Soundfile {soundfile} added to microphone {mic_name}.")
            return
    print(f"Microphone {mic_name} not found.")


def read_mics() -> list[dict[str, Union[str, float]]]:
    with open(os.path.join(dirname, "microphones.json"), "r") as file:
        mics = json.load(file)
    for mic in mics:
        if 'soundfile' in mic:
            mic['soundfile'] = os.path.join(base_path, mic['soundfile'])
    return mics


def write_mics(mics: list[dict[str, Union[str, float]]]) -> None:
    for mic in mics:
        if 'soundfile' in mic:
            mic['soundfile'] = os.path.relpath(mic['soundfile'], base_path)
    with open(os.path.join(dirname, "microphones.json"), "w") as file:
        file.write(json.dumps(mics, indent=4))
