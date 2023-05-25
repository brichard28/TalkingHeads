""" Generate a square wave on pin1 of DLP-IO8-G """

from time import perf_counter
from serial import Serial
import time

dlp = Serial(port='ASIO Fireface USB', baudrate=115200)  # open serial port
# byte codes to control line 1:
ON1 = b'1'
OFF1 = b'Q'

# number of periods
NPERIODS = 1000

# Timing of the square wave
TIME_HIGH = 0.010   # 10ms pulse
TIME_LOW = 0.090    # send every 100ms
PERIOD = TIME_HIGH + TIME_LOW

onset_times = [ (PERIOD * i) for i in range(NPERIODS) ]

i = 0
while i < NPERIODS:
    if i == 0:
        t0 = perf_counter()

    # wait until the start of the next period
    while perf_counter() - t0 < onset_times[i]:
        None

    dlp.write(ON1)

    # busy wait for 'TIME_HIGH' seconds. This should be more accurate than time.sleep(TIME_HIGH)
    t1 = perf_counter()
    while perf_counter() - t1 < (TIME_HIGH):
        None

    dlp.write(OFF1)
    i = i + 1
    print(f"\r{i:4d}", end='')

time.sleep(TIME_LOW)
print()
print(f'{NPERIODS} periods of {PERIOD} seconds')
print('Total time-elapsed: ' + str(perf_counter() -t0))
dlp.close()         # close the port