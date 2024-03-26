from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import os
import math
import numpy as np
import time
import numpy as np
from scipy.optimize import least_squares
import sys

class Microphone:
    def __init__(self, id, sample_rate):
        self.id = id
        self.sample_rate = sample_rate
        self.current_audio_data = []
        self.current_timestamp = 0

    def set_test_id(self, id):
        self.test_id = id

    def append_data(self, data):
        """
        Adds all new data to the end of existing data
        """
        self.current_audio_data.extend(data)

    def set_timestamp(self, timestamp):
        self.current_timestamp = timestamp

    def save(self, test_id):
        """
        Save audio data to a file on the form output/test_id/microphoneX_timestamp.txt
        """
        # TODO: change to .wav file
        if test_id == 0:
            return False

        try:
            f = open(
                f"{OUTPUT_FOLDER}/test_{test_id}/{self.id}_{self.current_timestamp}.txt", "w+")
            # TODO: This has to be optimized
            print("audio data", self.current_audio_data)
            f.write(''.join(map(str, self.current_audio_data)))
            f.close()
        except:
            return False

        self.current_timestamp = 0
        self.current_audio_data = []

        return True

ARGS = sys.argv[1:] # OUTPUT_FOLDER
OUTPUT_FOLDER = ARGS[0] 
app = Flask(__name__, static_folder='public', static_url_path='')

perf_counter = time.perf_counter()
print("preftcounter", perf_counter)
microphones: dict[int, Microphone] = {}
socketio = SocketIO(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/start_test/<test_id>')
def start_test(test_id):
    emit('start_test', test_id, broadcast=True, namespace="/")
    return {"msg": f"starting test {test_id}"}

@socketio.on('newMicrophone')
def handle_new_microphone(data):
    # Function to handle new user connection

    microphone_id = data.get('id') or 0
    sample_rate = data.get('sample_rate') or 44100

    microphones[request.sid] = Microphone(microphone_id, sample_rate)

    print(f'New microphone connected: {microphone_id}')

@socketio.on('audioData')
def handle_audio_data(data):
    if request.sid in microphones:
        microphone = microphones[request.sid]
        microphone.append_data(data['data'])
        if microphone.current_timestamp == 0:
            microphone.set_timestamp(data["timestamp"])

@socketio.on('endOfData')
def save_data(test_id):
    for microphone in microphones.values():
        print("saving...")
        microphone.save(test_id)
        print("done saving")

@socketio.on('syncTime')
def handle_sync_time():
    # Function to handle sync time request from the client
    print("Sync requested")
    server_timestamp = time.perf_counter() - perf_counter
    emit('syncResponse', server_timestamp)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
