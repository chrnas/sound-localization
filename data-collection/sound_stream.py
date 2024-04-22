import socketio
import pyaudio
import time
# import wave
# import os
import zlib
# import sys
import ntplib
from collections import deque
from threading import Thread

# Configuration and initialization
ID = "mathias"
server_url = f"http://localhost:5000"
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
BUFFER_DURATION = 5
BUFFER_SIZE = int(RATE / CHUNK * BUFFER_DURATION)

audio = pyaudio.PyAudio()
buffer = deque(maxlen=BUFFER_SIZE)

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, frames_per_buffer=CHUNK)

sio = socketio.Client()
ntp_client = ntplib.NTPClient()

initial_ntp_time = ntp_client.request('pool.ntp.org', version=3).tx_time
initial_perf_time = time.perf_counter()


def record_continuously():
    """
    Continuously record audio from the microphone and update the buffer.
    """
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            buffer.append(data)
    except KeyboardInterrupt:
        print("Recording stopped")


@sio.on('start_test')
def handle_start_test(data):
    """
    Handle the 'start_test' event from the server, which includes the start time for recording.
    Uses the initial NTP time and perf_counter to wait until the specified start time.
    """
    test_id = data['test_id']
    start_time = data['start_time']

    while True:
        current_time = initial_ntp_time + \
            (time.perf_counter() - initial_perf_time)
        if current_time >= start_time:
            break
        if current_time >= start_time - 1:
            recorded_data = b"".join(buffer)

    compressed_data = zlib.compress(recorded_data)
    chunk_size = CHUNK

    for i in range(0, len(compressed_data), chunk_size):
        sio.emit('audioData', {
                 'data': compressed_data[i:i + chunk_size], 'test_id': test_id, 'timestamp': current_time})

    sio.emit('endOfData', {'test_id': test_id})


@sio.event
def connect():
    """
    Handle connection to the server.
    """
    print("Connected to the server.")
    sio.emit('newMicrophone', {'id': ID, 'sample_rate': RATE})


@sio.event
def disconnect():
    """
    Handle disconnection from the server.
    """
    print("Disconnected from the server.")


if __name__ == "__main__":

    sio.connect(server_url)

    record_thread = Thread(target=record_continuously)
    record_thread.start()

    sio.wait()
    record_thread.join()
