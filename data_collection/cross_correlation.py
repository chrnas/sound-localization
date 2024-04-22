import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import correlate
import os


def load_wav(filename):
    # Load a WAV file, returning the sample rate and data
    rate, data = wavfile.read(filename)
    # Normalize data to float in range -1 to 1 if it's not already
    if data.dtype == np.int16:
        data = data.astype(np.float32) / np.iinfo(np.int16).max
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / np.iinfo(np.int32).max
    return rate, data


def plot_cross_correlation(data1, data2):

    # Perform cross-correlation
    correlation = correlate(data1, data2, mode='full')

    # Generate lag times
    lags = np.arange(-len(data2) + 1, len(data1))

    # Find the peak in cross-correlation
    peak_index = np.argmax(np.abs(correlation))
    peak_lag = lags[peak_index]

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(lags, correlation, label='Cross-correlation')
    plt.axvline(x=peak_lag, color='r', linestyle='--', label='Peak lag')
    plt.title('Cross-Correlation between Two Audio Signals')
    plt.xlabel('Lag')
    plt.ylabel('Correlation Coefficient')
    plt.legend()
    plt.show()

    return peak_lag


def find_wav_files(directory):

    files = os.listdir(directory)

    wav_files = [file for file in files if file.endswith('.wav')]
    if len(wav_files) < 2:
        raise ValueError("There are less than two WAV files in the directory.")
    return wav_files


def calculate_time_difference(peak_lag, rate):
    return peak_lag / rate


directory = "output/test_12_aligned"

wav_files = find_wav_files(directory)
wav_files.sort()  # Optional: Sort the files if needed

rate1, data1 = load_wav("output/test_11_aligned/output2.wav")
rate2, data2 = load_wav("output/test_11_aligned/output3.wav")

if rate1 != rate2:
    raise ValueError("Sample rates do not match!")

if len(data1.shape) == 2:
    data1 = data1[:, 0]
if len(data2.shape) == 2:
    data2 = data2[:, 0]

peak_lag = plot_cross_correlation(data1, data2)
time_difference = calculate_time_difference(peak_lag, rate1)

print(f"The peak correlation occurs at a lag of {peak_lag} samples.")
print(f"Time difference between the peaks: {time_difference:.6f} seconds.")
