import scipy
from scipy.io.wavfile import write
import wave
import numpy as np

RECORDING_FREQ = 44100  # MIC recording frequency
LOWER_FREQ = 10000      # Start frequency ocf chirp
UPPER_FREQ = 20000      # End frequecy of chirb OBS: should be less than 2 bandwiths (I think)
TIME_ARR = np.linspace(0, 1, RECORDING_FREQ)  # List of sample timestamps

freq_ar = [10, 20, 40, 80, 100, 200, 400, 800, 1000, 2000, 4000, 8000, 10000, 20000]


for i in range(len(freq_ar)-1):

    chirp = scipy.signal.chirp(TIME_ARR, freq_ar[i], 1, freq_ar[i+1]) # Create chirp signal

    with wave.open('Resources/chirp' + str(freq_ar[i]) + '-' + str(freq_ar[i+1]) + '.wav', mode="wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(1)
        wav_file.setnframes(RECORDING_FREQ)
        wav_file.setframerate(RECORDING_FREQ)
        wav_file.writeframes(chirp)

    # write('Resources/chirp' + str(freq_ar[i]) + '-' + str(freq_ar[i+1]) + '.wav', RECORDING_FREQ, chirp)