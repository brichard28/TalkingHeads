# -*- coding: utf-8 -*-
"""
Created on Wed May 24 13:47:11 2023

@author: Lab User
"""

# -*- coding: utf-8 -*-

# Copyright (c) 2010-2012 Christopher Brown
#
# This file is part of Psylab.
#
# Psylab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Psylab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Psylab.  If not, see <http://www.gnu.org/licenses/>.
#
# Bug reports, bug fixes, suggestions, enhancements, or other 
# contributions are welcome. Go to http://code.google.com/p/psylab/
# for more information and to contribute. Or send an e-mail to:
# cbrown1@pitt.edu.
#
# Psylab is a collection of Python modules for handling various aspects
# of psychophysical experimentation. Python is a powerful programming
# language that is free, open-source, easy-to-learn, and cross-platform,
# thus making it extremely well-suited to scientific applications.
# There are countless modules written by other scientists that are
# freely available, making Python a good choice regardless of your
# particular field. Consider using Python as your scientific platform.
#

# A Gustav experiment file!

import os, sys
import time
import numpy as np
import matplotlib.pyplot as plt
import psychopy
# import matlab.engine
# import matlab
import sounddevice as sd
from scipy.io.wavfile import write


# import spyral


import serial

# TRIGGER STUFF

sd.default.device = 'ASIO Fireface USB'
# import serial.tools.list_ports
# ports = serial.tools.list_ports.comports()
#
# for port, desc, hwid in sorted(ports):
#     print("{}:{}[{}]".format(port,desc,hwid))
# port = serial.Serial(port = 'COM4', baudrate = 115200)
trigger_sent = False

#eng = matlab.engine.start_matlab()
framerate = 44100
time = np.linspace(0,5)
stim = float(100) * np.sin(2.0*np.pi*float(440)*(time/framerate))
plt.plot(stim)
trig = np.ones(np.shape(stim))
print(np.shape(stim))
print(np.shape(trig))
send_to_triggy = np.transpose(np.stack((stim,trig)))
print(np.shape(send_to_triggy))
sd.play(send_to_triggy,44100)
# Devices = dict()
# Devices = eng.playrec('getDevices')[0,:]
# print(Devices)
# eng.playrec('init',44100,0,-1,20,-1);
# eng.playrec('play',matlab.double(send_to_triggy.tolist()),[1,2,3,4,5,6])
#eng.playrec('init',44100,0,-1,20,-1)

# Devices=eng.playrec('getDevices')
# print(Devices)
# if eng.isempty(Devices):
#     print('There are no devices available using the selected host APIs.\nPlease make sure the RME is powered on!')
# else:
#     i=1
#     while ~strcmp(Devices(i).name,'ASIO Fireface USB') and i <= length(Devices):
#         i=i+1
#
# fs = Devices[i].defaultSampleRate
# playDev = Devices[i].deviceID
#
# print('Success! Connected')

# for n_triggers in range(5):
#     x = 27
#     ConditionCode = bytearray(x)
#    # port.write(str.encode('hello', encoding='ascii', errors='strict'))
#     port.write([0,0,0,0,1,1,1,1,1])
#     time.sleep(0.2)
#     port.write(str.encode('0', encoding='ascii', errors='strict'))
#     trigger_sent = True
#     print('Sent trigger!')
#     time.sleep(1)
#

#port.close()