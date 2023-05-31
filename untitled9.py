# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:53:23 2023

@author: maana
"""

import vlc
import self

self.Instance = vlc.Instance("--verbose 9")
self.player = self.Instance.media_player_new()

devices = []
mods = self.player.audio_output_device_enum()

if mods:
    mod = mods
    while mod:
        mod = mod.contents
        devices.append(mod.device)
        mod = mod.next
        
vlc.libvlc_audio_output_device_list_release(mods)

self.player.audio_output_device_set(None, devices[0])  # this is the part I change on each run of the code.