import socketio
import pyaudio
import numpy as np
import time

# SocketIO client setup
sio = socketio.Client()
server_url = "http://localhost:5000"  # Adjust as needed
init_perf = time.perf_counter()

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SOUND_THRESHOLD = 0.15


client_send_time = None  # Initialize client_send_time


@sio.event
def connect():
    # Handle connection to the server
    print("Connected to the server.")
    name = "Mathias"
    xCoordinate = 10
    yCoordinate = 0
    sio.emit('newUser', {
             'name': name,
             'xCoordinate': xCoordinate,
             'yCoordinate': yCoordinate}
             )
    sync_time()


@sio.event
def disconnect():
    # Handle disconnection from the server
    print("Disconnected from the server.")


def sync_time():
    # Send a message to the server to synchronize time
    global client_send_time
    client_send_time = time.perf_counter() - init_perf  # Use perf_counter here
    sio.emit('syncTime')


@sio.on('syncResponse')
def handle_sync_response(server_time):
    # Calculate clock offset by comparing server time with client time
    global clock_offset, client_send_time
    client_receive_time = time.perf_counter() - init_perf  # Use perf_counter here

    round_trip_time = client_receive_time - client_send_time
    estimated_server_time_at_client_receive = server_time + round_trip_time / 2
    clock_offset = estimated_server_time_at_client_receive - client_receive_time

    print(f"Clock offset adjusted: {clock_offset} seconds.")

# Audio processing functions


def calculate_rms(buffer):
    return np.sqrt(np.mean(np.square(buffer)))


def main():
    sio.connect(server_url)

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    print("Listening for audio. Press Ctrl+C to stop.")
    last_triggered_time = None
    debounce_interval = 0.3

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            float_data = np.frombuffer(data, dtype=np.float32)

            # Comments here are for debouncing and sound thresholding but not active since we are streaming data

            # rms_value = calculate_rms(float_data)

            current_time = time.perf_counter() - init_perf  # Use perf_counter here
            # if rms_value > SOUND_THRESHOLD:
            #   if last_triggered_time is None or (current_time - last_triggered_time) > debounce_interval:
            timestamp = current_time + clock_offset
            sio.emit('audioData', {
                     'data': float_data.tolist(), 'timestamp': timestamp})
            last_triggered_time = current_time

    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        sio.disconnect()


if __name__ == "__main__":
    clock_offset = 0
    main()
