# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 11:02:02 2023

@author: Benjamin Richardson and Maanasa Guru Adimurthy
"""

from pydub import AudioSegment




start_time1 = 2000 
end_time1 = 2837 
start_time2 = 2000 
end_time2 = 3104
audio_file1 = AudioSegment.from_file("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Structured Sentences F1_Mp3/Kathy gives nine old chairs_1.wav", format="wav")
audio_file2=AudioSegment.from_file("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Structured Sentences F2_Mp3/Allen got sixty large houses_1.wav", format="wav")
audio_frame1 = audio_file1[start_time1:end_time1]
audio_frame2 = audio_file2[start_time2:end_time2]

panned_audio_matchedleft1 = audio_frame1.pan(-1)
panned_audio_mismatchleft1= audio_frame1.pan(1)
panned_audio_matchedright1=audio_frame1.pan(1)
panned_audio_mismatchright1=audio_frame1.pan(-1)


panned_audio_matchedright2 = audio_frame2.pan(1)
panned_audio_mismatchright2= audio_frame2.pan(-1)
panned_audio_matchedleft2 = audio_frame2.pan(-1)
panned_audio_mismatchleft2= audio_frame2.pan(1)  

panned_audio_matchedleft1.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Chairs_F1_matchedleft.wav", format="wav")
panned_audio_mismatchleft1.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Chairs_F1_mismatchedleft.wav", format="wav")
panned_audio_matchedright1.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Chairs_F1_matchedright.wav", format="wav")
panned_audio_mismatchright1.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Chairs_F1_mismatchedright.wav", format="wav")

panned_audio_matchedright2.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Houses_F2_matchedright.wav", format="wav")
panned_audio_mismatchright2.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Houses_F2_mismatchedright.wav", format="wav")
panned_audio_matchedleft2.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Houses_F2_matchedleft.wav", format="wav")
panned_audio_mismatchleft2.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Houses_F2_mismatchedleft.wav", format="wav")

