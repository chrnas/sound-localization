import socketio
import pyaudio
import numpy as np
import time
import sys

ARGS = sys.argv[1:] # IP, ID
IP = ARGS[0]
ID = ARGS[1]

# SocketIO client setup
sio = socketio.Client()
server_url = f"http://{IP}:5000"  # Adjust as needed
init_perf = time.perf_counter()

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SOUND_THRESHOLD = 0.15
RECORD_TIME = 5

client_send_time = None  # Initialize client_send_time
current_test = 0

def main():
    sio.connect(server_url)

    while True:
        global current_test
        data = []
        if current_test != 0:  # Check if a new test should start
            data = record_audio()
            print("Sending audio data to server")

        current_time = time.perf_counter() - init_perf  # Use perf_counter here
        timestamp = current_time + clock_offset
        
        while len(data) > 0:
            sio.emit('audioData', {
            'data': data.tolist()[:CHUNK], 'test_id': current_test, 'timestamp': timestamp})
            data = data[CHUNK:]
            print('sent chunk')
        if current_test != 0:
            sio.emit('endOfData', 0)
            current_test = 0  # Reset current_test
            print("Finished sending audio data to server")

# Audio processing functions


def record_audio():
    """
    Record audio for RECORD_TIME, seconds
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    print(f"Recording for {RECORD_TIME} seconds")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_TIME)):
        data = stream.read(CHUNK)
        frames.append(np.frombuffer(data, dtype=np.float32))

    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    return np.concatenate(frames)

def sync_time():
    """
    Send a message to the server to synchronize time.
    """
    global client_send_time
    client_send_time = time.perf_counter() - init_perf  # Use perf_counter here
    sio.emit('syncTime')

@sio.on('start_test')
def start_test(test_id):
    global current_test
    current_test = test_id

@sio.on('start_test_new')
def start_test(test_id):

    while True:
        data = []
        if test_id != 0:  # Check if a new test should start
            data = record_audio()
            print("Sending audio data to server")

        current_time = time.perf_counter() - init_perf  # Use perf_counter here
        timestamp = current_time + clock_offset
        
        while len(data) > 0:
            sio.emit('audioData', {
            'data': data.tolist()[:CHUNK], 'test_id': test_id, 'timestamp': timestamp})
            data = data[CHUNK:]
            print('sent chunk')
        if test_id != 0:
            sio.emit('endOfData', test_id)
            test_id = 0  # Reset current_test
            print("Finished sending audio data to server")

@sio.on('syncResponse')
def handle_sync_response(server_time):
    # Calculate clock offset by comparing server time with client time
    global clock_offset, client_send_time
    client_receive_time = time.perf_counter() - init_perf  # Use perf_counter here

    round_trip_time = client_receive_time - client_send_time
    estimated_server_time_at_client_receive = server_time + round_trip_time / 2
    clock_offset = estimated_server_time_at_client_receive - client_receive_time

    print(f"Clock offset adjusted: {clock_offset} seconds.")

@sio.event
def connect():
    # Handle connection to the server
    print("Connected to the server.")
    sio.emit('newMicrophone', {'id': ID, 'sample_rate': RATE})
    sync_time()

@sio.event
def disconnect():
    # Handle disconnection from the server
    print("Disconnected from the server.")

if __name__ == "__main__":
    clock_offset = 0
    main()
