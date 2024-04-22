import wave
import os
import numpy as np
from matplotlib import pyplot as plt


def open_wav_file(path):
    """Open a WAV file and return its audio data as a NumPy array."""
    with wave.open(path, 'rb') as wav_file:
        num_frames = wav_file.getnframes()
        audio_data = wav_file.readframes(num_frames)
        audio_data = np.frombuffer(audio_data, np.int16)
    return audio_data


def parse_time_stamps(file_name):
    """Parse timestamps from the filename assuming they are right before the extension."""
    try:
        base_name = os.path.basename(file_name)
        timestamp_str = base_name.split('_')[-1].split('.')[0]
        return float(timestamp_str)
    except ValueError:
        print(f"Error parsing timestamp for {file_name}. Using default 0.0")
        return 0.0


def plot_audio_data(audio_data_list, labels, colors):
    """Plot audio data for multiple files."""
    fig, axes = plt.subplots(len(audio_data_list), 1, figsize=(8, 6))
    for i, audio_data in enumerate(audio_data_list):
        time = np.arange(len(audio_data))
        axes[i].plot(time, audio_data, color=colors[i])
        axes[i].set_title(labels[i])
    plt.show()


def save_to_wav(file_path, audio_data, sample_rate=44100):
    """Save modified audio data to a WAV file."""
    with wave.open(file_path, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16 bits per sample
        wav_file.setframerate(sample_rate)  # Sample rate
        wav_file.writeframes(audio_data.astype(np.int16).tobytes())


if __name__ == "__main__":
    folder = "output/test_11"
    files = [os.path.join(folder, file) for file in os.listdir(
        folder) if os.path.isfile(os.path.join(folder, file))]

    timestamps = [parse_time_stamps(file) for file in files]
    earliest_time = min(timestamps)
    latest_time = max(timestamps)
    sample_rate = 44100

    audio_data_list = [open_wav_file(file) for file in files]
    modified_audio_data_list = []

    for timestamp, audio_data in zip(timestamps, audio_data_list):
        start_delay = int(sample_rate * (timestamp - earliest_time))
        if timestamp != latest_time:
            end_trim = int(sample_rate * (latest_time - timestamp))
            audio_data = audio_data[start_delay:-end_trim]
        else:
            audio_data = audio_data[start_delay:]
        modified_audio_data_list.append(audio_data)

    for i, audio_data in enumerate(modified_audio_data_list):
        print(len(audio_data))
        save_to_wav(f"{folder}_aligned/output{i+1}.wav", audio_data)
