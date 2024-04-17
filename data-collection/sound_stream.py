import socketio
import pyaudio
import time
import wave
import os
import zlib
import sys
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
BUFFER_DURATION = 5  # Buffer duration in seconds
# Number of chunks in the buffer
BUFFER_SIZE = int(RATE / CHUNK * BUFFER_DURATION)

audio = pyaudio.PyAudio()
buffer = deque(maxlen=BUFFER_SIZE)  # Deque to hold audio chunks

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, frames_per_buffer=CHUNK)

sio = socketio.Client()
ntp_client = ntplib.NTPClient()


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


def get_ntp_time():
    """
    Retrieve the current time from an NTP server.
    """
    response = ntp_client.request('pool.ntp.org', version=3)
    return response.tx_time


@sio.on('start_test')
def handle_start_test(data):
    """
    Handle the 'start_test' event from the server, which includes the start time for recording.
    Use NTP time and perf_counter to accurately wait until the start time.
    """
    test_id = data['test_id']
    start_time = data['start_time']

    initial_ntp_time = get_ntp_time()
    initial_perf_time = time.perf_counter()

    # Wait using perf_counter to reach the precise start time
    while True:
        current_time = initial_ntp_time + \
            (time.perf_counter() - initial_perf_time)
        if current_time >= start_time:
            break
        time.sleep(0.001)  # Microphone read could be blocked, however unsure.

    # Convert buffer to bytes and compress
    recorded_data = b"".join(buffer)
    compressed_data = zlib.compress(recorded_data)
    chunk_size = CHUNK

    # Send compressed audio data in chunks to the server
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
    # Connect to the server
    sio.connect(server_url)
    # Start recording continuously in a separate thread
    record_thread = Thread(target=record_continuously)
    record_thread.start()
    # Keep the SocketIO client running
    sio.wait()
    record_thread.join()
