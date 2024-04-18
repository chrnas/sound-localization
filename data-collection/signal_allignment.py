import wave
from matplotlib import pyplot as plt
import os
import numpy as np


def open_wav_file(path):
    with wave.open(path, 'rb') as wav_file:
        num_frames = wav_file.getnframes()
        audio_data = wav_file.readframes(num_frames)
        audio_data = np.frombuffer(audio_data, np.int16)

    return audio_data


def parse_time_stamps(file_name):
    timestamp_str_list = file_name.split('_')[-1].split('.')
    timestamp_str = timestamp_str_list[0] + '.' + timestamp_str_list[1]

    timestamp = float(timestamp_str)

    return timestamp


if __name__ == "__main__":

    folder = "output/"

    files = [folder+file for file in os.listdir(folder) if 
             os.path.isfile(os.path.join(folder, file))]

    timestamps = [parse_time_stamps(file) for file in files]

    diff = max(timestamps) - min(timestamps)

    sample_rate = 44100

    samples_to_remove = 44100 * diff

    print(samples_to_remove)
    maxindex = np.argmax(timestamps)
    minindex = np.argmin(timestamps)
    audio_data_array = []
    audio_data_1 = open_wav_file(files[0])
    audio_data_array.append(audio_data_1)
    audio_data_2 = open_wav_file(files[1])
    audio_data_array.append(audio_data_2)

    time_1 = np.arange(len(audio_data_1))
    time_2 = np.arange(len(audio_data_2))

    modified_audio_data_1 = audio_data_array[maxindex][:-int(samples_to_remove)]
    modified_audio_data_2 = audio_data_array[minindex][int(samples_to_remove):]

    print(len(audio_data_1))    
    print(len(audio_data_2))
    print(len(modified_audio_data_1))
    print(len(modified_audio_data_2))

    plt.plot(time_1, modified_audio_data_1)
    plt.show()
    plt.plot(time_2, modified_audio_data_2)
    plt.show()
