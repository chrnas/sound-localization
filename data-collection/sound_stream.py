import scipy.fft
import socketio
import pyaudio
import time
import wave
from playsound import playsound
import scipy
import os
import zlib
import sys
import TidsförskjutningBeräkning

ARGS = sys.argv
IP = ARGS[1]
ID = ARGS[2]

# SocketIO client setup
sio = socketio.Client()
server_url = f"http://{IP}:5000"

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 7
OUTPUT_FOLDER = "output_local"

# Global variables for synchronization
client_send_time = None
clock_offset = 0
chirp_time = 0
chirp_distance = 0


def record_audio(start_time):
    """
    Wait until the specified start time and then record audio for a predefined duration.
    """
    # Wait until the local performance counter reaches the specified start time
    while time.perf_counter() < start_time + clock_offset:
        time.sleep(0.001)  # Sleep briefly to avoid busy waiting

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Recording...")

    frames = []
    record_start_time = time.perf_counter()
    while time.perf_counter() - record_start_time < RECORD_SECONDS:
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return b''.join(frames)


def save_wav(test_id, timestamp, data):
    """
    Save the recorded audio data to a WAV file.
    """
    folder_path = os.path.join(OUTPUT_FOLDER, f"test_{test_id}")
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{ID}_{timestamp}.wav")

    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(data)

    print(f"Audio saved as {file_path}")


@sio.on('start_test')
def handle_start_test(data):
    """
    Handle the 'start_test' event from the server, which includes the start time for recording.
    """
    test_id = data['test_id']
    start_time = data['start_time']  # Server-provided start time for recording

    print(f"Received start_test signal for test {test_id}. Start time: {start_time}")

    # Record audio starting at the server-specified time
    recorded_data = record_audio(start_time + chirp_time)
    compressed_data = zlib.compress(recorded_data)

    # Send the recorded and compressed audio data back to the server in chunks
    chunk_size = CHUNK  # Adjust the chunk size as needed
    for i in range(0, len(compressed_data), chunk_size):
        sio.emit('audioData', {
                 'data': compressed_data[i:i + chunk_size], 'test_id': test_id, 'timestamp': start_time})

    # Notify the server that all data has been sent
    sio.emit('endOfData', test_id)

    # Optionally, save the recorded audio locally
    save_wav(test_id, start_time, recorded_data)


@sio.on('playSyncSound')
def play_sync_audio(data):
    playsound("../Resources/chirp" + data['freq_range'] + ".wav")


@sio.on('detectSyncSound')
def handle_sync_response(data):
    """
    Handle the syncResponse event from the server, which includes the server's timestamp.
    Adjust the clock offset based on the server's timestamp and the round-trip time.
    """
    start_freq = data['start_freq']
    end_freq = data['end_freq']

    chirp_wav = TidsförskjutningBeräkning.Wav_file("../Recources/chirp" + str(start_freq) + "-" + str(end_freq) + ".wav")

    recording_start = time.perf_counter()
    audio = record_audio(-clock_offset)

    audio_wav = TidsförskjutningBeräkning.Wav_file()

    audio_wav.audioVectorData = list(audio)
    audio_wav.audio_data_size(len(audio))

    offset = TidsförskjutningBeräkning.calc_offset(audio_wav, chirp_wav, True)

    chirp_time = recording_start + offset - (chirp_distance/343)


def sync_time():
    """
    Emit a syncTime event to the server to synchronize time.
    """
    global client_send_time
    client_send_time = time.perf_counter()
    sio.emit('syncTime')


@sio.event
def connect():
    """
    Handle connection to the server.
    """
    print("Connected to the server.")
    # Register this microphone/client with the server
    sio.emit('newMicrophone', {'id': ID, 'sample_rate': RATE})
    # Synchronize time with the server
    sync_time()


@sio.event
def disconnect():
    """
    Handle disconnection from the server.
    """
    print("Disconnected from the server.")


if __name__ == "__main__":
    # Connect to the server
    print(server_url)
    sio.connect(server_url)
    sio.wait()
