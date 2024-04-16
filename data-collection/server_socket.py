# echo-server.py

import socket
import wave
import pyaudio
from threading import Thread
import flask
import os
from time import perf_counter

app = flask.Flask(__name__)
init_perf = perf_counter()


HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 5000  # Port to listen on (non-privileged ports are > 1023)


def handle_client(conn, id):
    with conn:
        print(f"Connected by {addr}")
        data = bytes()
        while True:
            new_data = conn.recv(1024)
            data += new_data
            print(f'sent data from: {id}')
            # print(data)
            if not new_data:
                with wave.open(f'test_{id}.wav', 'wb') as wf:
                    RATE = 44100
                    wf.setnchannels(1)
                    wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
                    wf.setframerate(RATE)
                    # print(self.current_audio_data)
                    wf.writeframes(bytes(data))
                    print(f'converted to wav from: {id}')
                break


@app.route('/sync')
def sync_time():
    """
    Send a message to the server to synchronize time.
    """
    server_time = perf_counter() - init_perf
    return str(server_time)


if __name__ == "__main__":

    port = int(os.getenv('PORT', 6000))
    flask_thread = Thread(target=app.run, kwargs={
                          "host": '0.0.0.0', "port": port})
    flask_thread.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Listening...")
        s.bind(("0.0.0.0", PORT))
        s.listen(3)
        client_conns = []
        client_threads = []
        while True:
            conn, addr = s.accept()
            client_conns.append(conn)

            if len(client_conns) < 3:
                continue

            for id, conn in enumerate(client_conns):
                conn.send(b'start')
                thread = Thread(target=handle_client,
                                args=(client_conns[id], id))
                thread.start()
                client_threads.append(thread)
