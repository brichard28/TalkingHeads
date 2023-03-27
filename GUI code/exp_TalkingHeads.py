# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 14:50:15 2023

@author: Benjamin Richardson and Maanasa Guru Adimurthy
"""

import matlab.engine
import time
import os
from moviepy.editor import *
import vlc


SubID = input('Enter Subject ID: ')

eng_instruct = matlab.engine.start_matlab()


# Present subject with instructions
eng_instruct.instructiongui(nargout=0)
while not eng_instruct.workspace['release']:
    time.sleep(1)
    
eng_instruct.quit()

n_trials = 6
itrial = 0

eng_trial = matlab.engine.start_matlab()

all_responses_this_subject = []

while itrial < n_trials:
    
    
    # Present Video
    filename = "C:\\Users\\benri\\Documents\\GitHub\\TalkingHeads\\stim\\" + SubID + "trial_" + str(itrial) + ".mp4"
    os.add_dll_directory('C:/Program Files/VideoLAN/VLC')

    media_player = vlc.MediaPlayer()
    media = vlc.Media(os.path.abspath(filename))
    media_player.set_fullscreen(True)

    media_player.set_media(media)
    media_player.set_position(0.5)
    release = False
    
    media_player.play()

    time.sleep(5)

    media_player.stop()
    
    # Collect Response

    eng_trial.test21(nargout=0)
    
    curr_response = eng_trial.workspace['resp'];
    all_responses_this_subject.append(curr_response);
    
    itrial += 1

