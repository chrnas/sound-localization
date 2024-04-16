import socket
import flask
import os
from threading import Thread
from time import perf_counter

HOST = 'localhost'
PORT = 1235

app = flask.Flask(__name__)


if __name__ == "__main__":

    print("Öpnnar port")
    port = int(os.getenv('PORT', PORT))
    print("Potatissallad")
    flask_thread = Thread(target=app.run, kwargs={
                          "host": '0.0.0.0', "port": port})
    print("köttbullar")
    flask_thread.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        
        print("Listening...")
        
        s.bind(("0.0.0.0", PORT))
        s.listen(3)
        
        while (True):
            conn, addr = s.accept()
            with conn:
                data = bytearray()
                
                while (True):
                    new_data = conn.recv(1024)
                    data += new_data
                    while (data(0) != 0xA5):
                        del data[0]
                    if (len(data) >= 10):
                        if (data(9) == 0xA6):
                            
                            time_diff = perf_counter() - float(data[1:8])
                            print(time_diff*1000)
                        del data[0]