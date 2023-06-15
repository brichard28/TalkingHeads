# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 09:24:12 2023

@author: maana
"""


import serial
import time

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)

for i in range(50):
    line = ser.readline()   # read a byte
    if line:
        string = line.decode()  # convert the byte string to a unicode string
        num = int(string) # convert the unicode string to an int
        print(num)

ser.close()

