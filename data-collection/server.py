from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os
import numpy as np
import time
import numpy as np
from scipy.optimize import least_squares
import sys
import os
import matplotlib.pyplot as plt

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
        print('start_saving')
        # TODO: change to .wav file
        print(test_id)
        if test_id == 0:
            return False
        folder_path = f"{OUTPUT_FOLDER}/test_{test_id}"
        f = open(f"{self.id}_{self.current_timestamp}.txt", "w+")
        if not os.path.exists(os.path.normpath(folder_path)):
            os.makedirs(os.path.normpath(folder_path))
        f = open(
            os.path.normpath(f"{folder_path}/{self.id}_{self.current_timestamp}.txt"), "w+")
        # TODO: This has to be optimized
        audio_data = ''.join(map(str, self.current_audio_data))
        
        #Create and save plot
        x_data = np.arange(len(self.current_audio_data))
        y_data = self.current_audio_data
        plt.plot(x_data, y_data)
        plt.savefig('public/pic.png')
        
        #Write and close files
        f.write(audio_data)
        print('writing data')
        f.close()
        
        self.current_timestamp = 0
        self.current_audio_data = []
        return app.send_static_file('pic.png')

ARGS = sys.argv[1:] # OUTPUT_FOLDER
OUTPUT_FOLDER = ARGS[0] 
app = Flask(__name__, static_folder='public', static_url_path='')

perf_counter = time.perf_counter()
print("preftcounter", perf_counter)
microphones: dict[int, Microphone] = {}
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        test_id = request.form['test_id']
        # Do something with the input_text, for example, print it
        print("Input text:", test_id)
        start_test_new(test_id)
    return render_template('index.html', name='app')

@app.route('/start_test/<test_id>')
def start_test(test_id):
    print('Test ID:', test_id)
    emit('start_test', test_id, broadcast=True, namespace="/")
    return {"msg": f"starting test {test_id}"}

@app.route('/start_test_new/<test_id>')
def start_test_new(test_id):
    print('Test ID:', test_id)
    emit('start_test_new', test_id, broadcast=True, namespace="/")
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
        # TODO: This has to be optimized
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
