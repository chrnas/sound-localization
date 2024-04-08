# echo-client.py

import socket
import pyaudio
import requests
from time import perf_counter

HOST = "localhost"  # The server's hostname or IP address
PORT = 5000  # The port used by the server

client_send_time = perf_counter()  # Use perf_counter here
server_time = requests.get(
    "http://localhost:5000/sync")  # Start test with ID 1

server_time = float(server_time.text)
print(f"Server time: {server_time}")

# Calculate clock offset by comparing server time with client time
client_receive_time = perf_counter()  # Use perf_counter here

round_trip_time = client_receive_time - client_send_time
estimated_server_time_at_client_receive = server_time + round_trip_time / 2
clock_offset = estimated_server_time_at_client_receive - client_receive_time

clock = perf_counter() + clock_offset

print(f"Clock offset adjusted: {clock} seconds.")
print(clock)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    if s.recv(1024) == b'start':
        print('hello world')
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5

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
    s.sendall(b''.join(frames))
