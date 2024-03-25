### CURRENTLY NOT CORRECT FORMATED WITH THE SERVER, USE intex_once.html ### 

## NEED TO BE RE WRITTEN IN ACCORDANCE TO THE SERVER ## SEE SCRIPT2.JS for the correct format.

import socketio
import pyaudio
import numpy as np
from datetime import datetime, timedelta
from time import perf_counter


# SocketIO client setup
sio = socketio.Client()
server_url = "http://localhost:3000"  # Adjust as needed
init_perf = perf_counter()

FORMAT = pyaudio.paFloat32  
CHANNELS = 1
RATE = 44100
CHUNK = 32 
SOUND_THRESHOLD = 0.5



# Root mean square calculation
def calculate_rms(audio_data):
    return np.sqrt(np.mean(np.square(audio_data)))

@sio.event
def connect():
    print("Connected to the server.")
    name = "Mathias"
    sio.emit('newUser', {'name': name, 'xCoordinate': 1, 'yCoordinate': 2})
    sync_time()  

# TODO FIX THIS FUNCTION
@sio.event
def sync_time():
    client_time = perf_counter() - init_perf
    sio.emit('syncTime')

#TODO FIX THIS FUNCTION
@sio.on('syncResponse')
def handle_sync_response(data):
    pass

@sio.event
def disconnect():
    print("Disconnected from the server.")

from datetime import datetime, timedelta


# TODO FIX THIS FUNCTION
def main():
    sio.connect(server_url)

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Listening for audio. Press Ctrl+C to stop.")
    last_triggered_time = None  # Keep track of the last time the event was triggered
    debounce_interval = timedelta(seconds=0.2)  # Set the debounce interval (e.g., 1 second)

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            float_data = np.frombuffer(data, dtype=np.float32).tolist()

            rms_value = calculate_rms(float_data)
            current_time = datetime.now()
            
            if rms_value > SOUND_THRESHOLD:
                if last_triggered_time is None or (current_time - last_triggered_time) > debounce_interval:
                    adjusted_timestamp = current_time + clock_offset
                    timestamp = adjusted_timestamp.isoformat()
                    sio.emit('audioData', {'data': float_data, 'timestamp': timestamp})
                    last_triggered_time = current_time  # Update the last triggered time

    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        sio.disconnect()


if __name__ == "__main__":
    main()
