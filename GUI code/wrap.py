# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 11:13:25 2023

@author: maana
"""

import matlab.engine
import time
import os
from moviepy.editor import *
import vlc

eng_instruct = matlab.engine.start_matlab()


# Present subject with instructions
eng_instruct.instructiongui(nargout=0)
while not eng_instruct.workspace['release']:
    time.sleep(1)
    
eng_instruct.quit()

n_trials = 2
itrial = 1

SubID = input('Enter Subject ID: ')

while itrial <= n_trials:
    
    eng_trial = matlab.engine.start_matlab()
    
    # Present Video
    filename = "C:\\Users\\benri\\Documents\\PhD Year 2\\Maanasa Mentorship\\stim\\" + SubID + "trial_" + str(itrial) + ".mp4"
    os.add_dll_directory('C:/Program Files/VideoLAN/VLC')

    media_player = vlc.MediaPlayer()
    media = vlc.Media(os.path.abspath(filename))

    media_player.set_media(media)

    media_player.play()

    time.sleep(5)

    media_player.stop()
    
    # Collect Response
    eng_trial.test21(nargout=0)
    
    itrial += 1

