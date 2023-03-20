# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 11:41:36 2023

@author: maana
"""

import vlc
import os
os.add_dll_directory('C:/Program Files/VideoLAN/VLC')
media= vlc.MediaPlayer("C:/Users/maana/Desktop/Research/Stimuli/Stevi Sentences -- Sensimetrics/Structured Sentences F2_MP4/Allen bought nine pretty sofas_1.mp4")
media.play()