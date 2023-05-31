# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:02:42 2023

@author: maana
"""

import time
from typing import List

import vlc


def vlc_set_device_test(filename: str):
    # creating a vlc instance
    vlc_instance: vlc.Instance = vlc.Instance()
    player: vlc.MediaPlayer = vlc_instance.media_player_new()
    media: vlc.Media = vlc_instance.media_new(filename)
    player.set_media(media)

    # list devices
    device_ids: List[bytes] = []
    mods = player.audio_output_device_enum()
    if mods:
        index = 0
        mod = mods
        while mod:
            mod = mod.contents
            desc = mod.description.decode('utf-8', 'ignore')
            print(f'index = {index}, desc = {desc}')
            device_ids.append(mod.device)

            mod = mod.next
            index += 1

    # free devices
    vlc.libvlc_audio_output_device_list_release(mods)

    # hard code device
    pc_speaker = device_ids[4]
    headset = device_ids[5]

    # play music to default device



    # set output device
    player.audio_output_device_set(pc_speaker, headset)
    player.play()
    time.sleep(5)
    # don't call player.stop()!!
    player.pause()

    # now music is playing from headset
    #player.play()
    #time.sleep(5)

    player.stop()

if __name__ == '__main__':
    vlc_set_device_test('D:\\Experiments\\TalkingHeads\\stim\\s_trig4\\trig4_trial_0_cond_ match left.mp4')