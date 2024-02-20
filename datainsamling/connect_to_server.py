import socketio
import pyaudio
import numpy as np
from datetime import datetime, timedelta

# SocketIO client setup
sio = socketio.Client()
server_url = "http://localhost:3000"  # Adjust as needed

clock_offset = timedelta(0)  

# Audio capture setup
FORMAT = pyaudio.paFloat32  # Use floating-point format
CHANNELS = 1
RATE = 44100
CHUNK = 2048  # Match JavaScript buffer size

# Connect to the server
@sio.event
def connect():
    print("Connected to the server.")
    # Sending a 'newUser' event to the server with example user data
    name = "Mathias"
    sio.emit('newUser', {'name': name, 'xCoordinate': 1, 'yCoordinate': 2})
    sync_time()  # Initiate clock synchronization

@sio.event
def sync_time():
    client_send_time = datetime.now()
    sio.emit('syncTime', {'timestamp': client_send_time.isoformat()})

@sio.on('syncResponse')
def handle_sync_response(data):
    global clock_offset 
    client_receive_time = datetime.now()
    client_send_time = datetime.fromisoformat(data['clientTimestamp'])
    server_time = datetime.fromisoformat(data['serverTimestamp'])
    
    round_trip_time = client_receive_time - client_send_time
    estimated_server_time = server_time + (round_trip_time / 2)
    
    clock_offset = estimated_server_time - client_receive_time
    print(f"Clock offset: {clock_offset.total_seconds()} seconds. Adjust your clock accordingly.")

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
            data = stream.read(CHUNK, exception_on_overflow=False)
            float_data = np.frombuffer(data, dtype=np.float32).tolist()  
            adjusted_timestamp = datetime.now() + clock_offset
            timestamp = adjusted_timestamp.isoformat()
            sio.emit('audioData', {'data': float_data, 'timestamp': timestamp})
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        sio.disconnect()

if __name__ == "__main__":
    main()
