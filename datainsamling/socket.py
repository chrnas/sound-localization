import websocket
import threading
import pyaudio
import json
import numpy as np
from datetime import datetime

# Configuration for audio streaming
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

def audio_int16_to_float32(data):
    return np.frombuffer(data, dtype=np.int16).tolist()

# Establish a connection to the WebSocket server
def on_message(ws, message):
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        name = input("Enter your name: ")
        xCoordinate = input("Enter your X coordinate: ")
        yCoordinate = input("Enter your Y coordinate: ")

        # Inform the server of the new user and their coordinates
        ws.send(json.dumps({'type': 'newUser', 'name': name, 'xCoordinate': xCoordinate, 'yCoordinate': yCoordinate}))

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        print("Recording...")

        try:
            while True:
                data = stream.read(CHUNK, exception_on_overflow=False)
                int_data = audio_int16_to_float32(data)
                timestamp = datetime.now().isoformat()
                ws.send(json.dumps({'type': 'audioData', 'name': name, 'data': int_data, 'timestamp': timestamp}))
        except KeyboardInterrupt:
            # Stop the stream and close everything
            stream.stop_stream()
            stream.close()
            p.terminate()
            ws.close()
            print("Recording stopped.")

    thread = threading.Thread(target=run)
    thread.start()

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("localhost:5000",
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
