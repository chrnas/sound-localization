# Adjust the base path and positioning imports
import ntplib
import zlib
import pyaudio
import wave
import time
import os
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request  # jsonify
from threading import Thread
import numpy as np
import sys
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_path)
from positioning.calcfunctions.receiver import Receiver
from positioning.tdoa import TDOAMethod


# Define directories

initial_time = time.perf_counter()
ntp_client = ntplib.NTPClient()
response = ntp_client.request('pool.ntp.org', version=3)

last_loud_noise_time = 0
loud_noise_cooldown = 5


class Microphone:
    def __init__(self, id, sample_rate, latitude, longitude):
        self.id = id
        self.sample_rate = sample_rate
        self.current_audio_data = b""
        self.current_timestamp = 0
        self.latitude = latitude
        self.longitude = longitude
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
        
        for mic in microphones.values():
            mic.current_audio_data = b""
            mic.current_timestamp = 0

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
    if not microphone.data_submitted:
        #thread = Thread(target=microphone.save, args=(test_id,))
        #thread.start()
        microphone.data_submitted = True
        # Check if all microphones have submitted their data
        if all(mic.data_submitted for mic in microphones.values()):
            print("All microphones have submitted their data.")
            triangulate()

    else:
        print("Data for this microphone has already been submitted)")


@ socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    if request.sid in microphones:
        del microphones[request.sid]


def remove_inf_and_nans(data):
    # Check if there are NaNs or Infs before replacing
    if np.isnan(data).any() or np.isinf(data).any():
        original_shape = data.shape
        data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
        num_replacements = np.prod(original_shape) - np.count_nonzero(data)
    return data


def triangulate():
    tdoa_method = TDOAMethod()
    mic_data = {}
    
    # Wait for all audio data to be received
    time.sleep(0.5)
    for mic in microphones.values():

        decompressed = zlib.decompress(mic.current_audio_data)
        float_samples = np.frombuffer(
            decompressed, dtype=np.int16).astype(np.float32)
        
        float_samples=remove_inf_and_nans(float_samples)

        receiver = Receiver([mic.latitude, mic.longitude])

        mic_data[receiver] = float_samples

    if mic_data:
        source_position = tdoa_method.find_source(mic_data, sample_rate = 44100)
        print(f"Estimated source position: {source_position}")
    else:
        print("No valid microphone data available to estimate source position.")


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
