from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__, static_folder='public', static_url_path='')

socketio = SocketIO(app)

class AudioData:
    def __init__(self, data, timestamp):
        self.data = data
        self.timestamp = timestamp

    def __repr__(self):
        return f'AudioData(data={len(self.data)}, timestamp={self.timestamp})'

class User:
    def __init__(self, name, xCoordinate=None, yCoordinate=None):
        self.name = name
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.audio_data = []

    def add_audio_data(self, audio_data):
        if len(self.audio_data) >= 10:
            self.audio_data.pop(0)  
        self.audio_data.append(audio_data)  

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
    xCoordinate = data.get('xCoordinate') 
    yCoordinate = data.get('yCoordinate')
    microphones[request.sid] = User(name, xCoordinate, yCoordinate)
    print(f'New user connected: {microphones[request.sid]}')

@socketio.on('audioData')
def handle_audio_data(data):
    new_data = AudioData(data=data['data'], timestamp=data.get('timestamp'))
    if request.sid in microphones:
        microphones[request.sid].add_audio_data(new_data)
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
