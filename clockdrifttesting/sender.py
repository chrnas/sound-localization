import requests
from time import sleep, perf_counter

start_time = perf_counter()
print(requests.get("http://192.168.125.69:5000/sync").text)
server_start_time = float(requests.get("http://192.168.125.69:5000/sync").text)
counter = 0
while True:
    server_time = float(requests.get("http://192.168.125.69:5000/sync").text)
    server_lapsed_time = server_time - server_start_time
    client_lapsed_time = perf_counter() - start_time
    print("Client time: " + str(client_lapsed_time) + " Server time: " + str(server_lapsed_time))
    print("Time diff: " + str(server_lapsed_time - client_lapsed_time))
    sleep(60)
