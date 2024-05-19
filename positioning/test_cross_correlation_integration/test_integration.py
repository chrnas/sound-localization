
from positioning.cross_correlation import calc_offset_wav
from scipy.io import wavfile
import os
import warnings


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
