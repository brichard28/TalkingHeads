# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 09:24:12 2023

@author: maana
"""


import serial
import time

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM4', 115200, timeout=1)
time.sleep(2)

while True:
    line = ser.readline()   # read a byte
    print(line)
    if line:
        string = line.decode()  # convert the byte string to a unicode string
        #num = int(string) # convert the unicode string to an int
        print(string)


#while True:
 #   if ser.in_waiting > 0:
  #      data = ser.readline().decode().rstrip()
   #     print(data)

ser.close()

