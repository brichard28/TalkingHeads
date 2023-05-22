# -*- coding: utf-8 -*-
"""
Created on Sun May 14 20:24:28 2023

@author: maana
"""
from pydub import AudioSegment

start_time1 = 1970 
end_time1 = 2837 
audio_file1 = AudioSegment.from_file("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Structured Sentences F1_Mp3/Kathy gives nine old chairs_1.wav", format="wav")
audio_frame1 = audio_file1[start_time1:end_time1]
panned_audio_matchedleft1 = audio_frame1.pan(-1)
panned_audio_mismatchleft1= audio_frame1.pan(1)
panned_audio_matchedright1=audio_frame1.pan(1)
panned_audio_mismatchright1=audio_frame1.pan(-1)
panned_audio_matchedleft1.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Chairs_F1_matchedleft.wav", format="wav")
panned_audio_mismatchleft1.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Chairs_F1_mismatchedleft.wav", format="wav")
panned_audio_matchedright1.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Chairs_F1_matchedright.wav", format="wav")
panned_audio_mismatchright1.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Chairs_F1_mismatchedright.wav", format="wav")
