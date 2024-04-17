import requests
from time import sleep, perf_counter

start_time = perf_counter()
print(requests.get("http://192.168.125.69:5000/sync").text)
server_start_time = float(requests.get("http://192.168.125.69:5000/sync").text)
start_diff = server_start_time - start_time
counter = 0
time_diffs = []
while True:
    server_time = float(requests.get("http://192.168.125.69:5000/sync").text)
    server_lapsed_time = server_time - server_start_time
    client_lapsed_time = perf_counter() - start_time
    print("Client time: " + str(client_lapsed_time) +
          " Server time: " + str(server_lapsed_time))
    time_diffs.append(float(abs(client_lapsed_time - server_lapsed_time)))
    print("Time diff: " + str(time_diffs[-1]))
    
    print("avg diff: " + str(sum(time_diffs)/len(time_diffs)))
    print("largest diff: " + str(max(time_diffs)))
    sleep(1)
