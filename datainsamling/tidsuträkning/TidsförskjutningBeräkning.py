import numpy as np
from scipy.io import wavfile
from scipy.signal import resample

from scipy.fftpack import fft, ifft

#-----------------------------------------------------
# Helper functions and classes

class Wav_file:
    # Initializer for Wav_file class
    def __init__(self, filename: str):
        # Create blank wav object 
        if filename == '':
            self.audioVectorData = []
            self.sampling_rate = 0
        else:
            self.filename: str = filename
            # Load WAV file data and sampling rate on instantiation
            self.audioVectorData, self.sampling_rate = self.read_wav_file(filename) 

    # Function to read WAV file and return its data and sampling rate
    def read_wav_file(self, filename: str) -> tuple[int, list[float]]:
        sampling_rate, audioVectorData = wavfile.read(filename)
        return audioVectorData, sampling_rate
    
    # Function to resample the WAV file to a new sampling rate
    def resample_wav(self, sample_rate: int) -> None:
        # Resample audio data to the new sampling rate
        self.audioVectorData = resample(self.audioVectorData, sample_rate)
        # Update the object's sampling rate to the new rate
        self.sampling_rate = sample_rate

    def audio_data_size(self) -> int:
        return len(self.audioVectorData)

    # Function to save the object's audio data and sampling rate to a new WAV file
    def save(self, output_filename: str) -> None:
        audio_array = np.array(self.audioVectorData, dtype=np.float32)  # or np.float32 depending on your audio data format
        wavfile.write(output_filename, self.sampling_rate, audio_array)

def create_wav_object(audio_data: list[float], sample_rate: int) -> Wav_file:
    wav_file = Wav_file('')
    wav_file.filename = 'data_stream'
    wav_file.audioVectorData = audio_data
    wav_file.sampling_rate = sample_rate
    return wav_file


    

# Function to calculate the number of shifted samples between two WAV files
def calc_shifted_samples(wav1: Wav_file, wav2: Wav_file) -> int:
    # Extract audio vector data from both WAV files
    audio1VectorData = wav1.audioVectorData
    audio2VectorData = wav2.audioVectorData

    # Perform cross-correlation between the two audio vectors
    correlation = np.correlate(audio1VectorData, audio2VectorData, mode='full')
    # Find the index of the maximum correlation value
    max_corr_index = np.argmax(correlation)
    # Calculate the shift amount based on the max correlation index
    shift = max_corr_index - (len(audio1VectorData) - 1)
    return shift

def calc_shifted_samples_fft(wav1: Wav_file, wav2: Wav_file) -> int:
    # Extract audio vector data from both WAV files
    audio1VectorData = wav1.audioVectorData
    audio2VectorData = wav2.audioVectorData

    # Perform FFT on both audio vectors
    fft_audio1 = fft(audio1VectorData, n=2*max(len(audio1VectorData), len(audio2VectorData))-1)
    fft_audio2 = fft(np.flipud(audio2VectorData), n=2*max(len(audio1VectorData), len(audio2VectorData))-1)
    
    # Perform element-wise multiplication of the two FFT results
    fft_result = fft_audio1 * fft_audio2
    
    # Perform inverse FFT to get the cross-correlation in the time domain
    correlation = np.abs(ifft(fft_result))

    # Find the index of the maximum correlation value
    max_corr_index = np.argmax(correlation)
    
    # Calculate the shift amount based on the max correlation index
    shift = max_corr_index - len(audio1VectorData) + 1
    
    return shift

# Function to resample WAV files to the highest sampling rate between them
def resample_to_highest(wav1: Wav_file, wav2: Wav_file) -> tuple[Wav_file, Wav_file]:
    # Determine the highest sampling rate between the two WAV files
    if wav1.sampling_rate <= wav2.sampling_rate:
        highest_sampling_rate = wav2.sampling_rate  # Corrected typo here from wav2,sampling_rate to wav2.sampling_rate
        wav1.resample_wav(highest_sampling_rate)
    else:
        highest_sampling_rate = wav1.sampling_rate
        wav2.resample_wav(highest_sampling_rate)
   
    return wav1, wav2 

#----------------------------------------------------------------- 
# Running code

# Function to calculate the time offset between two WAV files
def calc_offset(wav1: Wav_file, wav2: Wav_file) -> float:
    # Check if the sampling rates are the same
    if wav1.sampling_rate == wav2.sampling_rate:
        shifted_samples = calc_shifted_samples_fft(wav1, wav2)
    else:
        # Resample the WAV files to the highest sampling rate if they differ
        wav1, wav2 = resample_to_highest(wav1, wav2)
        shifted_samples = calc_shifted_samples_fft(wav1, wav2)

    # Calculate the time offset based on the number of shifted samples
    shifted_time = shifted_samples * (1 / wav1.sampling_rate)

    return shifted_time

# Function to calculate the time offset between two WAV files given their filenames
def calc_offset_wav(wav_file1: str, wav_file2: str) -> float:
    wav1 = Wav_file(wav_file1)
    wav2 = Wav_file(wav_file2)
    return calc_offset(wav1, wav2)

if __name__ == '__main__':
    # Define filenames for the WAV files to compare
    filenameSnap1 = 'testSnap1.wav' 
    filenameSnap2 = 'testSnap2.wav' 
    # Print the calculated time offset between the two WAV files
    print(calc_offset_wav(filenameSnap1, filenameSnap2))

