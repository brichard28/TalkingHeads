# -*- coding: utf-8 -*-
"""
Created on Wed May 31 09:39:12 2023

@author: maana
"""

import vlc
import os
import time


file= "C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\stim\\s_trig4\\trig4_trial_0_cond_ match left.mp4"
os.add_dll_directory('C:/Program Files/VideoLAN/VLC')
inst=vlc.Instance()
media_player = vlc.MediaPlayer()
media = vlc.Media(os.path.abspath(file))
media_player.set_media(media)
media_player.play()
time.sleep(5)
media_player.stop()

value = media_player.audio_output_device_enum()
  
# printing value
print("Audio Output Devices: ")
print(value)

aud= vlc.libvlc_audio_output_list_get(inst)
ii= vlc.libvlc_audio_output_device_enum(media_player)
dev= 'ASIO Fireface USB'
pp= vlc.libvlc_audio_output_set(media_player,dev)

