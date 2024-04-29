import numpy as np
from scipy.io import wavfile
from scipy.signal import resample
from scipy.fftpack import fft, ifft

# -----------------------------------------------------

# Helper Functions and Classes


class WavFile:
    """
    A class for representing and manipulating WAV files.
    """

    def __init__(self, filename: str):
        """
        Initializes the WavFile object.

        Args:
            filename (str): The name of the WAV file to be loaded.
        """

        if filename == '':
            self.audioVectorData = []
            self.sampling_rate = 0
        else:
            self.filename: str = filename
            # Load WAV file data and sampling rate on instantiation

            self.audioVectorData, self.sampling_rate = self.read_wav_file(
                filename)

    def read_wav_file(self, filename: str) -> tuple[list[float], int]:
        """
        Reads a WAV file and returns its data and sampling rate.

        Args:
            filename (str): The name of the file to read.

        Returns:
            tuple[list[float], int]: The audio data and sampling rate.
        """
        sampling_rate, audioVectorData = wavfile.read(filename)
        return audioVectorData, sampling_rate

    # Function to resample the WAV file to a new sampling rate

    def resample_wav(self, sample_rate: int) -> None:
        """
        Resamples the WAV file to a new sampling rate.

        Args:
            sample_rate (int): The new sampling rate.
        """
        self.audioVectorData = resample(self.audioVectorData, sample_rate)
        self.sampling_rate = sample_rate

    def audio_data_size(self) -> int:
        """
        Returns the size of the audio data vector.

        Returns:
            int: The size of the audio data.
        """
        return len(self.audioVectorData)

    def save(self, output_filename: str) -> None:
        """
        Saves the audio data to a WAV file.

        Args:
            output_filename (str): The name of the output file.
        """

        # or np.float32 depending on your audio data format
        audio_array = np.array(self.audioVectorData, dtype=np.float32)
        wavfile.write(output_filename, self.sampling_rate, audio_array)


def create_wav_object(audio_data: list[float], sample_rate: int) -> WavFile:
    """
    Creates a WavFile object from audio data and a sampling rate.

    Args:
        audio_data (list[float]): The audio data.
        sample_rate (int): The sampling rate.

    Returns:
        WavFile: The created WavFile object.
    """
    wav_file = WavFile('')

    wav_file.filename = 'data_stream'
    wav_file.audioVectorData = audio_data
    wav_file.sampling_rate = sample_rate
    return wav_file


def calc_shifted_samples(wav1: WavFile, wav2: WavFile) -> int:
    """
    Calculates the number of shifted samples between two WAV files.

    Args:
        wav1 (WavFile): The first WAV file.
        wav2 (WavFile): The second WAV file.

    Returns:
        int: The number of shifted samples.
    """
    audio1VectorData = wav1.audioVectorData
    audio2VectorData = wav2.audioVectorData
    correlation = np.correlate(audio1VectorData, audio2VectorData, mode='full')
    max_corr_index = np.argmax(correlation)
    shift = max_corr_index - (len(audio1VectorData) - 1)
    return shift


def calc_shifted_samples_fft(wav1: WavFile, wav2: WavFile) -> int:
    """
    Calculates the number of shifted samples between two WAV files using FFT.

    Args:
        wav1 (WavFile): The first WAV file.
        wav2 (WavFile): The second WAV file.

    Returns:
        int: The number of shifted samples.
    """

    audio1VectorData = wav1.audioVectorData
    audio2VectorData = wav2.audioVectorData

    # Perform FFT on both audio vectors
    fft_audio1 = fft(audio1VectorData, n=2 *
                     max(len(audio1VectorData), len(audio2VectorData))-1)
    fft_audio2 = fft(np.flipud(audio2VectorData), n=2 *
                     max(len(audio1VectorData), len(audio2VectorData))-1)

    # Perform element-wise multiplication of the two FFT results
    fft_result = fft_audio1 * fft_audio2

    # Perform inverse FFT to get the cross-correlation in the time domain

    correlation = np.abs(ifft(fft_result))
    max_corr_index = np.argmax(correlation)

    # Calculate the shift amount based on the max correlation index
    shift = max_corr_index - len(audio1VectorData) + 1

    return shift

# Function to resample WAV files to the highest sampling rate between them


def resample_to_highest(wav1: WavFile, wav2: WavFile) -> tuple[WavFile, WavFile]:
    """
    Resamples two WAV files to the highest sampling rate between them.

    Args:
        wav1 (WavFile): The first WAV file.
        wav2 (WavFile): The second WAV file.

    Returns:
        tuple[WavFile, WavFile]: The resampled WAV files.
    """
    # Determine the highest sampling rate between the two WAV files
    if wav1.sampling_rate <= wav2.sampling_rate:
        # Corrected typo here from wav2,sampling_rate to wav2.sampling_rate

        highest_sampling_rate = wav2.sampling_rate
        wav1.resample_wav(highest_sampling_rate)
    else:
        highest_sampling_rate = wav1.sampling_rate
        wav2.resample_wav(highest_sampling_rate)
    return wav1, wav2


def trim_lists_to_same_length(list1: list, list2: list) -> tuple[list, list]:
    """
    Trims the longer of two lists to make both lists the same length.

    Args:
        list1 (List): The first list.
        list2 (List): The second list.

    Returns:
        Tuple[List, List]: A tuple containing both lists, with the longer list trimmed
                            to match the length of the shorter list.
    """
    # Determine the length of the shorter list
    shorter_length = min(len(list1), len(list2))

    # Trim both lists to the determined shorter length
    trimmed_list1 = list1[:shorter_length]
    trimmed_list2 = list2[:shorter_length]

    return trimmed_list1, trimmed_list2

# -----------------------------------------------------------------
# Running code


def identify_first_sound(sounds: list[list[float]]):
    """
    Identify the first sound file based on cross-correlation time differences.
    The one with the largest negative time difference when compared to others is the first.

    Args:
        sounds (list of list of float): A list where each item is a sound sample list.

    Returns:
        int: Index of the first sound sample list detected.
    """
    min_time_difference = float('inf')
    first_index = 0

    # Choose one sound as a reference, compare it against all others
    reference_sound = sounds[0]

    for i in range(1, len(sounds)):
        time_difference = calc_offset_from_samples(
            sounds[i], reference_sound)
        # If this sound starts before the current reference
        if time_difference < min_time_difference:
            min_time_difference = time_difference
            first_index = i

    # Adjust for the fact that the first sound might not be the reference
    if min_time_difference > 0:
        first_index = 0

    return first_index


def calc_offset(wav1: WavFile, wav2: WavFile) -> float:
    """
    Calculates the time offset between two WAV files.

    Args:
        wav1 (WavFile): The first WAV file.
        wav2 (WavFile): The second WAV file.

    Returns:
        float: The time offset in seconds.
    """

    if wav1.sampling_rate == wav2.sampling_rate:
        shifted_samples = calc_shifted_samples_fft(wav1, wav2)
    else:
        wav1, wav2 = resample_to_highest(wav1, wav2)
        shifted_samples = calc_shifted_samples_fft(wav1, wav2)
    shifted_time = shifted_samples * (1 / wav1.sampling_rate)
    return shifted_time


def calc_offset_wav(wav_file1: str, wav_file2: str) -> float:
    """
    Calculates the time offset between two WAV files given their filenames.

    Args:
        wav_file1 (str): The filename of the first WAV file.
        wav_file2 (str): The filename of the second WAV file.

    Returns:
        float: The time offset in seconds.
    """
    wav1 = WavFile(wav_file1)
    wav2 = WavFile(wav_file2)
    return calc_offset(wav1, wav2)


def calc_offset_from_samples(samples1, samples2, rate1=44100, rate2=44100,):
    """
    Calculates the time offset between two sets of audio samples and their sampling rates.

    Args:
        samples1 (list[float]): The audio samples of the first sound.
        rate1 (int): The sampling rate of the first sound.
        samples2 (list[float]): The audio samples of the second sound.
        rate2 (int): The sampling rate of the second sound.

    Returns:
        float: The time offset in seconds between the two sets of samples.
    """
    # Create WavFile objects from the provided samples and rates
    wav1 = create_wav_object(samples1, rate1)
    wav2 = create_wav_object(samples2, rate2)

    # Calculate and return the time offset using the existing functionality
    return calc_offset(wav1, wav2)


if __name__ == '__main__':
    # Define filenames for the WAV files to compare
    filenameSnap1 = 'testSnap1.wav'
    filenameSnap2 = 'testSnap2.wav'

    # Print the calculated time offset between the two WAV files
    print(calc_offset_wav(filenameSnap1, filenameSnap2))
