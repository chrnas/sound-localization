import socket
from time import sleep
from time import perf_counter

HOST = "192.168.125.246"  # The server's hostname or IP address
PORT = 7777  # The port used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    sleep(2)
    while True:
        client_send_time = perf_counter()
        s.send(0xA5)
        s.send(client_send_time)
        s.send(0xA6)
        sleep(1)
