import ntplib
import time

client = ntplib.NTPClient()
response = client.request('pool.ntp.org', version=3)
response.dest_time
print('offset:', time.ctime(response.offset))
print('timestamp:',response.tx_timestamp)
print('time:',response.tx_time)

