# echo-server.py

import socket
import wave
import pyaudio
import numpy as np

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 5000  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            with wave.open('test.wav','wb') as wf:
                RATE = 44100
                wf.setnchannels(1)
                wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(RATE)
                # print(self.current_audio_data)
                wf.writeframes(data)