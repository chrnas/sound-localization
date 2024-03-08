from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit
import os
import math
from datetime import datetime
from Multilaterate import Multilateration
import numpy as np
import time
import numpy as np
from scipy.optimize import least_squares

app = Flask(__name__, static_folder='public', static_url_path='')

perf_counter = time.perf_counter()
print("preftcounter", perf_counter)
socketio = SocketIO(app)


multilateration = Multilateration(v=343, delta_d=1, max_d=300)  # Example values

class AudioData:
    
    def __init__(self, data, timestamp):
        self.data = data
        self.timestamp = timestamp

    def RMS(self):
        # Calculate the root mean square of the audio data, good for calculating loudness
        return math.sqrt(sum([sample**2 for sample in self.data]) / len(self.data))

    def __repr__(self):
        return f'AudioData(data={len(self.data)}, timestamp={self.timestamp})'

class User:
    def __init__(self, name, xCoordinate=None, yCoordinate=None):
        self.name = name
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.audio_data = []
        self.distances = {} 
        self.last_timestamp = None

    def update_last_timestamp(self, timestamp):
        self.last_timestamp = timestamp

    def add_audio_data(self, audio_data):
        if len(self.audio_data) >= 10:
            self.audio_data.pop(0)
        self.audio_data.append(audio_data)

    def calculate_distances(self, users):
        for sid, user in users.items():
            if user != self:
                dx = self.xCoordinate - user.xCoordinate
                dy = self.yCoordinate - user.yCoordinate
                distance = math.sqrt(dx**2 + dy**2)
                self.distances[sid] = distance
    
    def get_last_audio_data(self):
        if len(self.audio_data) > 0:
            return self.audio_data[-1]
        return None

    def get_last_audio_data_timestamp(self):
        return self.last_timestamp
    
    def __repr__(self):
        return f'User(name={self.name}, xCoordinate={self.xCoordinate}, yCoordinate={self.yCoordinate}, audio_data_count={len(self.audio_data)})'

microphones = {}

def timestamps_to_tdoas(timestamps):
    reference_timestamp = min(timestamps)  # Use the earliest timestamp as reference
    tdoas = [timestamp - reference_timestamp for timestamp in timestamps]
    return tdoas

def broadcast_user_positions():
    users_data = [{'name': user.name, 'xCoordinate': user.xCoordinate, 'yCoordinate': user.yCoordinate} for user in microphones.values()]
    emit('updatePositions', users_data, broadcast=True)

@app.route('/')
def index():
    return app.send_static_file('index_once.html')

@socketio.on('connect')
def handle_connect():
    print(f'A user connected with ID: {request.sid}')
    emit('userConnected', {'id': request.sid}, broadcast=True, include_self=False)

@socketio.on('newUser')
def handle_new_user(data):
    name = data.get('name')
    xCoordinate = float(data.get('xCoordinate'))  
    yCoordinate = float(data.get('yCoordinate'))
    new_user = User(name, xCoordinate, yCoordinate)
    microphones[request.sid] = new_user

    new_user.calculate_distances(microphones)
    for sid, user in microphones.items():
        if sid != request.sid:
            user.calculate_distances(microphones)

    print(f'New user connected: {new_user}')
    broadcast_user_positions()

@socketio.on('audioData')
def handle_audio_data(data):
    
    #print("client", data["timestamp"])
    #print("server", time.perf_counter() - perf_counter)

    if request.sid in microphones:
        timestamp = data.get('timestamp')
        if timestamp:
            microphones[request.sid].last_timestamp = data["timestamp"]


        # Need to perfom check on the timestamps to see if they are in sync, debouncing and problems on client side could cause issues
        print("Location:" , calculate_sound_source())

@socketio.on('syncTime')
def handle_sync_time():
    print("Sync requested") 
    server_timestamp = time.perf_counter() - perf_counter 
    emit('syncResponse', server_timestamp)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in microphones:
        print(f'User {microphones[request.sid].name} disconnected')
        microphones.pop(request.sid, None)
    emit('userDisconnected', {'id': request.sid}, broadcast=True)

def calculate_sound_source():
    # Calculate the sound source position using the time differences of arrival

    speed_of_sound = 343  # 

    valid_mics = [mic for mic in microphones.values() if mic.get_last_audio_data_timestamp()]
    valid_mics.sort(key=lambda mic: mic.get_last_audio_data_timestamp())

    if len(valid_mics) < 2:
        print("Need at least two microphones to perform calculation")
        return None

    ref_time = valid_mics[0].get_last_audio_data_timestamp()

    distances = np.array([speed_of_sound * (mic.get_last_audio_data_timestamp() - ref_time) for mic in valid_mics])

    positions = np.array([[mic.xCoordinate, mic.yCoordinate] for mic in valid_mics])

    def equations(guess):
        x, y = guess
        return [(np.linalg.norm([x - pos[0], y - pos[1]]) - distance) for pos, distance in zip(positions, distances)]

    initial_guess = [0, 0]

    result = least_squares(equations, initial_guess)

    sound_source_position = np.round(result.x).astype(int)

    return sound_source_position



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000)) 
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
