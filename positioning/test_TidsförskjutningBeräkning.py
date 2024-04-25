import numpy as np
import warnings
import pytest
from scipy.io import wavfile
from TidsförskjutningBeräkning import create_wav_object, calc_shifted_samples_fft, calc_offset_wav
import os


@pytest.fixture
def example_wavfile():
    """
    Fixture to create a WavFile object for testing.
    """
    # Create a WavFile object with dummy data
    audio_data = np.sin(2 * np.pi * np.linspace(0, 1, 48000))
    sample_rate = 48000
    wav_file = create_wav_object(audio_data, sample_rate)
    return wav_file


def test_audio_data_size(example_wavfile):
    """
    Test if audio_data_size method returns the correct size.
    """
    assert example_wavfile.audio_data_size(
    ) == 48000, "Audio data size should be equal to 48000"


def test_resample_wav(example_wavfile):
    """
    Test if resample_wav method correctly changes the sampling rate.
    """
    example_wavfile.resample_wav(24000)
    assert example_wavfile.sampling_rate == 24000, "Sampling rate should be updated to 24000"
    # Note: This test does not check if the data was correctly resampled, just the sample rate change.


def test_calc_shifted_samples_fft():
    """
    Test calculation of shifted samples using FFT with identical files.
    """
    # Create two identical WavFile objects for testing
    audio_data = np.sin(2 * np.pi * np.linspace(0, 1, 48000))
    sample_rate = 48000
    wav_file1 = create_wav_object(audio_data, sample_rate)
    wav_file2 = create_wav_object(audio_data, sample_rate)
    assert calc_shifted_samples_fft(
        wav_file1, wav_file2) == 0, "Shifted samples should be 0 for identical audio"


def test_calc_offset_wav():
    """
    Test calculation of time offset between two WAV files using actual files.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", wavfile.WavFileWarning)

        # Assuming the test script is in the same directory as the WAV files
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file1 = os.path.join(dir_path, "testSnap1.wav")
        file2 = os.path.join(dir_path, "testSnap2.wav")

        # Expected delay between the files in seconds
        expected_delay = 0.174

        # Calculating the actual delay using the calc_offset_wav function
        actual_delay = calc_offset_wav(file1, file2)

        # Asserting that the actual delay is approximately equal to the expected delay
        # Allowing a small margin of error due to processing and rounding
        assert abs(actual_delay - expected_delay) < 0.001, f"Expected delay of {
            expected_delay}s, but got {actual_delay}s"
