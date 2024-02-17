from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
from flask import request
import os

app = Flask(__name__, static_folder='public', static_url_path='')

socketio = SocketIO(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@socketio.on('connect')
def handle_connect():
    print(f'A user connected with ID: {request.sid}')
    emit('userConnected', {'id': request.sid}, broadcast=True, include_self=False)

@socketio.on('audioData')
def handle_audio_data(data):
    emit('incomingAudioData', {'id': request.sid, 'name': data['name'], 'data': data['data']}, broadcast=True, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    print(f'User {request.sid} disconnected')
    emit('userDisconnected', {'id': request.sid}, broadcast=True)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    socketio.run(app, host='0.0.0.0', port=port)