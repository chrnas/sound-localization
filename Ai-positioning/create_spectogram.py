import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def create_spectrogram(wav_file_path, target_image_path):
    # Load the audio file
    y, sr = librosa.load(wav_file_path, sr=None)

    # Compute the spectrogram magnitude and phase
    S_full, phase = librosa.magphase(librosa.stft(y))

    # Convert to decibels
    S_db = librosa.amplitude_to_db(S_full, ref=np.max)

    # Create a figure without axis
    fig, ax = plt.subplots(figsize=(12, 4), frameon=False)
    plt.axis('off')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

    # Plot and save the spectrogram
    librosa.display.specshow(S_db, sr=sr, x_axis='time',
                             y_axis='log', cmap='gray_r')
    plt.savefig(target_image_path, bbox_inches='tight',
                pad_inches=0, dpi=300, format='png', transparent=True)
    plt.close()


# Usage
wav_file_path = 'microphone_1.wav'  # Path to the WAV file
# Path where the spectrogram image will be saved
target_image_path = 'spectrogram_grayscale2.png'
create_spectrogram(wav_file_path, target_image_path)
