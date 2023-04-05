# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 11:02:02 2023

@author: Benjamin Richardson and Maanasa Guru Adimurthy
"""

from pydub import AudioSegment




start_time1 = 0 
end_time1 = 800 
start_time2 = 0 
end_time2 = 700
audio_file1 = AudioSegment.from_file("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Structured Sentences F1_Mp3/Kathy gives nine old chairs_1.wav", format="wav")
audio_file2=AudioSegment.from_file("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Structured Sentences F2_Mp3/Allen got sixty large houses_1.wav", format="wav")
audio_frame1 = audio_file1[start_time1:end_time1]
audio_frame2 = audio_file2[start_time2:end_time2]

panned_audio1 = audio_frame1.pan(-1)
panned_audio2 = audio_frame2.pan(1)

panned_audiomismatch1= audio_frame1.pan(1)
panned_audiomismatch2= audio_frame2.pan(-1) 

panned_audio1.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Kathy_F1.wav", format="wav")
panned_audio2.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Allen_F2.wav", format="wav")

panned_audiomismatch1.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Kathy_F1_mismatch.wav", format="wav")
panned_audiomismatch2.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Allen_F2_mismatch.wav", format="wav")