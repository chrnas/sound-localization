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

from positioning.calcfunctions.receiver import Receiver
from positioning.calcfunctions import constants
from positioning.tdoa import calculate_time_differences
from positioning.TidsförskjutningBeräkning import calc_offset_from_samples


initial_time = time.perf_counter()
ntp_client = ntplib.NTPClient()
response = ntp_client.request('pool.ntp.org', version=3)

last_loud_noise_time = 0
loud_noise_cooldown = 2


class Microphone:
    def __init__(self, id, sample_rate, latitude, longitude):
        self.id = id
        self.sample_rate = sample_rate
        self.current_audio_data = b""
        self.current_timestamp = 0
        self.latitude = latitude
        self.longitude = longitude
        # Track if data has been submitted since the last loud noise
        self.data_submitted = False

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


@socketio.on('loudNoise')
def handle_loud_noise():
    global last_loud_noise_time, response, initial_time
    current_time = time.perf_counter()
    ntp_current_time = response.tx_time + (current_time - initial_time)

    if ntp_current_time - last_loud_noise_time > loud_noise_cooldown:
        last_loud_noise_time = ntp_current_time
        future_timestamp = ntp_current_time + 2.5
        emit('start_test', {'test_id': "test",
             'start_time': future_timestamp}, broadcast=True)

        # Reset data submission flag for all microphones
        for mic in microphones.values():
            mic.data_submitted = False

        print(
            f"Loud noise processed, emitting start test event for future timestamp: {future_timestamp}")
    else:
        print("Loud noise ignored due to server-wide cooldown.")


@socketio.on('newMicrophone')
def handle_new_microphone(data):
    # Function to handle new user connection

    microphone_id = data.get('id') or 0
    sample_rate = data.get('sample_rate') or 44100
    latitude = data.get('latitude') or 0
    longitude = data.get('longitude') or 0
    microphones[request.sid] = Microphone(
        microphone_id, sample_rate, latitude, longitude)

    print(
        f'New microphone connected: {microphone_id} with sample rate {sample_rate} and coordinates ({latitude}, {longitude})')


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
    test_id = 1  # Example test ID, replace with real logic if necessary
    if not microphone.data_submitted:
        print("Saving...")
        thread = Thread(target=microphone.save, args=(test_id,))
        thread.start()
        microphone.data_submitted = True
        # Check if all microphones have submitted their data
        if all(mic.data_submitted for mic in microphones.values()):
            print("All microphones have submitted their data.")

            # Triangulate the source of the sound

    else:
        print("Data for this microphone has already been submitted)")


@ socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    if request.sid in microphones:
        del microphones[request.sid]


def triangulate():
    # TODO Implement triangulation logic
    pass


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
