import socket
import time
import ntplib
from time import ctime

client = ntplib.NTPClient()
response = client.request('172.20.10.6', version=3)
time_str = ctime(response.tx_time)
print(response.offset)
print(time_str)