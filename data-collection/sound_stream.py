import socketio
import pyaudio
import numpy as np
import time
import sys
import wave
import os

ARGS = sys.argv[1:] # IP, ID
IP = ARGS[0]
ID = ARGS[1]

# SocketIO client setup
sio = socketio.Client()
server_url = f"http://{IP}:5000"  # Adjust as needed
init_perf = time.perf_counter()

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 15
OUTPUT_FILENAME = "output_client.wav"
OUTPUT_FOLDER = "output_local"

client_send_time = None  # Initialize client_send_time

def main():
    sio.connect(server_url)

    while True:
        pass

# Audio processing functions

def record_audio():
    """
    Record audio for RECORD_TIME, seconds
    """
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open stream
    stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    # Record audio data
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Recording finished.")

    # Stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return b''.join(frames)

def save_wav(test_id, timestamp, data):
    folder_path = f"{OUTPUT_FOLDER}/test_{test_id}"
    if not os.path.exists(os.path.normpath(folder_path)):
        os.makedirs(os.path.normpath(folder_path))

    with wave.open(os.path.normpath(f"{folder_path}/{ID}_{timestamp}.wav"),'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(RATE)
        # print(self.current_audio_data)
        wf.writeframes(bytes(data))

def sync_time():
    """
    Send a message to the server to synchronize time.
    """
    global client_send_time
    client_send_time = time.perf_counter() - init_perf  # Use perf_counter here
    sio.emit('syncTime')

@sio.on('start_test')
def start_test(test_id):
    data = []
    data = record_audio()
    print("Sending audio data to server")
    current_time = time.perf_counter() - init_perf  # Use perf_counter here
    timestamp = current_time + clock_offset
    
    save_wav(test_id, timestamp, data)
    while len(data) > 0:
        sio.emit('audioData', {
        'data': data[:CHUNK], 'test_id': test_id, 'timestamp': timestamp})
        data = data[CHUNK:]
    if test_id != 0:
        sio.emit('endOfData', test_id)
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
