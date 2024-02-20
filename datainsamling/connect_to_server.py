import socketio
import pyaudio
import numpy as np
from datetime import datetime

# SocketIO client setup
sio = socketio.Client()
server_url = "http://localhost:3000"  # Adjust as needed

# Audio capture setup
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Connect to the server
@sio.event
def connect():
    print("Connected to the server.")
    # Sending a 'newUser' event to the server with example user data
    sio.emit('newUser', {'name': 'PythonClient', 'xCoordinate': 1, 'yCoordinate': 2})

# Handle server disconnect
@sio.event
def disconnect():
    print("Disconnected from the server.")

def main():
    sio.connect(server_url)

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Streaming audio to the server. Press Ctrl+C to stop.")

    try:
        while True:
            data = stream.read(CHUNK)
            int_data = np.frombuffer(data, dtype=np.int16).tolist()  # Convert audio bytes to int16 list
            timestamp = datetime.now().isoformat()
            sio.emit('audioData', {'data': int_data, 'timestamp': timestamp})
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        sio.disconnect()

if __name__ == "__main__":
    main()
