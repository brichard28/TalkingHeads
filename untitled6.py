# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:22:58 2023

@author: maana
"""

import numpy as np
import sounddevice as sd
import time
import serial

# Samples per second
sps = 44100

# Frequency / pitch
freq_hz = 440.0

# Duration
duration_s = 1.0

# Attenuation so the sound is reasonable
atten = 0.1

# NumpPy magic to calculate the waveform
each_sample_number = np.arange(duration_s * sps)
waveform = np.sin(2 * np.pi * each_sample_number * freq_hz / sps)
waveform_quiet = waveform * atten
trigger_channel_3 = np.zeros(np.shape(waveform_quiet))
trigger_channel_3[0] = 0.03
#trigger_channel_3[452] = 0
trigger_channel_4 = np.zeros(np.shape(waveform_quiet))
trigger_channel_4[33000] = 0.03
trigger_channel_5 = np.zeros(np.shape(waveform_quiet))
trigger_channel_5[33000] = 0.03
waveform_quiet = np.transpose(np.stack(((waveform_quiet,waveform_quiet,trigger_channel_3,trigger_channel_4,trigger_channel_5))))
print(np.shape(waveform_quiet))
# Play the waveform out the speakers
sd.default.device = 'ASIO Fireface USB'
sd.play(waveform_quiet, sps,mapping=[1,2,3,4,5])
time.sleep(duration_s)
sd.stop()