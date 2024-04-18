import ntplib
import time

init_time = time.perf_counter()
client = ntplib.NTPClient()

# Assuming NTP server is run on the same machine

while True:
    start = time.perf_counter()
    ntp_response = client.request("pool.ntp.org", version=3)
    print(f"Time taken: {time.perf_counter() - start}")