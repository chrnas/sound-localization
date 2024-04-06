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
            self.audioVectorData, self.sampling_rate = self.read_wav_file(filename)

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
    fft_audio1 = fft(audio1VectorData, n=2 * max(len(audio1VectorData), len(audio2VectorData)) - 1)
    fft_audio2 = fft(np.flipud(audio2VectorData), n=2 * max(len(audio1VectorData), len(audio2VectorData)) - 1)
    fft_result = fft_audio1 * fft_audio2
    correlation = np.abs(ifft(fft_result))
    max_corr_index = np.argmax(correlation)
    shift = max_corr_index - len(audio1VectorData) + 1
    return shift


def resample_to_highest(wav1: WavFile, wav2: WavFile) -> tuple[WavFile, WavFile]:
    """
    Resamples two WAV files to the highest sampling rate between them.

    Args:
        wav1 (WavFile): The first WAV file.
        wav2 (WavFile): The second WAV file.

    Returns:
        tuple[WavFile, WavFile]: The resampled WAV files.
    """
    if wav1.sampling_rate <= wav2.sampling_rate:
        highest_sampling_rate = wav2.sampling_rate
        wav1.resample_wav(highest_sampling_rate)
    else:
        highest_sampling_rate = wav1.sampling_rate
        wav2.resample_wav(highest_sampling_rate)
    return wav1, wav2


# -----------------------------------------------------------------
# Interfacing Code

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




if __name__ == '__main__':
    # Define filenames for the WAV files to compare
    filenameSnap1 = 'testSnap1.wav'
    filenameSnap2 = 'testSnap2.wav'
    # Print the calculated time offset between the two WAV files
    print(calc_offset_wav(filenameSnap1, filenameSnap2))
