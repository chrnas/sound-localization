# 1. Timestampa och skicka chirp till server

# 3.  Ta emot och räkna ut timestamp. 
# 4. Synka klockan. Skicka sedan ut ngt för att mäta latens i nätverket. 


import socket
import pyaudio
import requests
import scipy
from time import perf_counter

HOST = "localhost"  # The server's hostname or IP address
PORT = 5000  # The port used by the server

RECORDING_FREQ = 44100
LOWER_FREQ = 10000
UPPER_FREQ = 20000
TIME_ARR = [1/44100 * i for i in range(RECORDING_FREQ)]

client_send_time = perf_counter()  # Use perf_counter here
server_time = requests.get(
    "http://localhost:6000/sync")  # Start test with ID 1

while server_time.status_code != 200:
    # Sleep for a short duration before checking again
    server_time = requests.get("http://localhost:6000/sync")


server_time = float(server_time.text)
print(f"Server time: {server_time}")

# Calculate clock offset by comparing server time with client time
client_receive_time = perf_counter()  # Use perf_counter here

first_chirp = scipy.signal.chirp(TIME_ARR, LOWER_FREQ, 1, UPPER_FREQ)

round_trip_time = client_receive_time - client_send_time

estimated_server_time_at_client_receive = server_time + round_trip_time / 2
clock_offset = estimated_server_time_at_client_receive - client_receive_time

clock = perf_counter() + clock_offset

HOST = "localhost"
PORT = 5000

client_send_time = perf_counter()
server_time_response = requests.get(f"http://{HOST}:{PORT}/sync")
server_time = float(server_time_response.text)
print(f"Server time: {server_time}")

client_receive_time = perf_counter()
round_trip_time = client_receive_time - client_send_time


# Synchronize client's clock with estimated server time
client_clock = perf_counter() + clock_offset


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    if s.recv(1024) == b'start':
        print(perf_counter() + clock_offset)
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