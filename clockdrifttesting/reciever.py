import socket
import struct
from time import perfcounter

HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 7777       # Port number

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print("Listening for incoming connections...")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            if data[0] == 0xA5 and data[-1] == 0xA6:
                # Unpack the timestamp between the markers
                , received_time = struct.unpack('!Bd', data[:9])
                server_time = perf_counter()
                time_drift = server_time - received_time
                print(f"Time drift: {time_drift * 1000:.2f} ms")