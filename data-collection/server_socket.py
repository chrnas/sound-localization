# echo-server.py

import socket
import wave
import pyaudio
from threading import Thread 

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
            #print(data)
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


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(3)
    id = 0
    client_conns = []
    client_threads = []
    while True:
        for id in range(3):
            conn, addr = s.accept()
            client_conns.append(conn)
        for id in range(3):
            client_conns[id].send(b'start')
            thread = Thread(target=handle_client, args=(client_conns[id], id))
            thread.start()
            client_threads.append(thread)
        
                
                
                
