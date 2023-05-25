# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:22:58 2023

@author: maana
"""

import serial

ser = serial.Serial('COM4', 9600)
ser.open()

trigger_data = b'TRIGGER'
ser.write(trigger_data)
ser.close()   