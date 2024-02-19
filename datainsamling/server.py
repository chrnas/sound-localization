from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit
import os
import math

app = Flask(__name__, static_folder='public', static_url_path='')

socketio = SocketIO(app)

class AudioData:
    def __init__(self, data, timestamp):
        self.data = data
        self.timestamp = timestamp

    def __repr__(self):
        return f'AudioData(data={len(self.data)}, timestamp={self.timestamp})'

    def RMS(self):
        return math.sqrt(sum([sample**2 for sample in self.data]) / len(self.data))

class User:
    def __init__(self, name, xCoordinate=None, yCoordinate=None):
        self.name = name
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.audio_data = []
        self.distances = {} 

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
        last_audio_data = self.get_last_audio_data()
        if last_audio_data:
            return last_audio_data.timestamp
        return None

    def __repr__(self):
        return f'User(name={self.name}, xCoordinate={self.xCoordinate}, yCoordinate={self.yCoordinate}, audio_data_count={len(self.audio_data)})'

microphones = {}

@app.route('/')
def index():
    return app.send_static_file('index.html')

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
        if sid != request.sid: # Don't send the new user to itself
            user.calculate_distances(microphones)

    print(f'New user connected: {new_user}')

@socketio.on('audioData')
def handle_audio_data(data):
    # TODO How to we check each microhpones timestamp and compare it to the other microphones timestamps?


    new_data = AudioData(data=data['data'], timestamp=data.get('timestamp'))
    if request.sid in microphones:
        microphones[request.sid].add_audio_data(new_data)

        rms = new_data.RMS()

        loudness_threshold = 0.2  
        
        print(f'Loudness: {rms}')

        if rms > loudness_threshold:
            print(f'Loud sound detected at {new_data.timestamp} from {microphones[request.sid].name}')


    emit('incomingAudioData', {'id': request.sid, 'name': microphones[request.sid].name, 'data': data['data']}, broadcast=True, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in microphones:
        print(f'User {microphones[request.sid].name} disconnected')
        microphones.pop(request.sid, None)
    emit('userDisconnected', {'id': request.sid}, broadcast=True)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # Updated default port to 5000
    socketio.run(app, host='0.0.0.0', port=port)
