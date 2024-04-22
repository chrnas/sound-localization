from threading import Thread
from flask import Flask, render_template, request  # jsonify
from flask_socketio import SocketIO, emit
import os
# import numpy as np
import time
# import numpy as np
# import sys
# import os
# import matplotlib.pyplot as plt
import wave
import pyaudio
import zlib
import ntplib

perf_counter = time.perf_counter()


class Microphone:
    def __init__(self, id, sample_rate):
        self.id = id
        self.sample_rate = sample_rate
        self.current_audio_data = b""
        self.current_timestamp = 0

    def set_test_id(self, id):
        self.test_id = id

    def append_data(self, data):
        """
        Adds all new data to the end of existing data
        """
        self.current_audio_data += data

    def set_timestamp(self, timestamp):
        self.current_timestamp = timestamp

    def save(self, test_id):
        """
        Save audio data to a file on the form
        output/test_id/microphoneX_timestamp.txt
        """
        print('start_saving')
        if test_id == 0:
            return False
        folder_path = f"{OUTPUT_FOLDER}/test_{test_id}"
        if not os.path.exists(os.path.normpath(folder_path)):
            os.makedirs(os.path.normpath(folder_path))

        with wave.open(os.path.normpath(f"{folder_path}/{self.id}_\
                      {self.current_timestamp}.wav"), 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(bytes(zlib.decompress(self.current_audio_data)))
        print(
            f"Audio saved as {OUTPUT_FOLDER}/test_{test_id}/{self.id}_\
                             {self.current_timestamp}.wav")

        self.current_timestamp = 0
        self.current_audio_data = b""


OUTPUT_FOLDER = "output"
app = Flask(__name__, static_folder='public', static_url_path='')

microphones: dict[int, Microphone] = {}
socketio = SocketIO(app, max_http_buffer_siz=1e10)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        test_id = request.form['test_id']
        # Do something with the input_text, for example, print it
        print("Input text:", test_id)
        start_test(test_id)
    return render_template('index.html', name='app')


# TODO Fix this for NTP
@app.route('/start_test/<test_id>')
def start_test(test_id):
    print('Test ID:', test_id)
    # Get current server time

    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('pool.ntp.org', version=3)
    current_time = response.tx_time
    future_timestamp = current_time + 2

    emit('start_test', {'test_id': test_id,
         'start_time': future_timestamp}, broadcast=True, namespace="/")

    return {"msg": f"starting test {test_id} at {future_timestamp}"}


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
    microphone = microphones[request.sid]
    print("saving...")
    thread = Thread(target=microphone.save, args=(test_id,))
    thread.start()
    # microphone.save(test_id)


# TODO Old stuff


@socketio.on('syncTime')
def handle_sync_time():
    # Function to handle sync time request from the client
    print("Sync requested")
    server_timestamp = time.perf_counter() - perf_counter
    emit('syncResponse', server_timestamp)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
