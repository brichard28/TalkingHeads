# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 18:02:58 2023

@author: maana
"""


from pydub import AudioSegment
import numpy as np

start_time1 = 1970 
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


# Function to apply a 10ms cosine ramp to the given audio segment
def apply_cosine_ramp(audio_segment):
    # Set the duration of the cosine ramp in seconds (10ms)
    ramp_duration = 0.01

    # Calculate the number of samples needed for the ramp
    num_samples = int(ramp_duration * audio_segment.frame_rate)

    # Generate the cosine ramp
    t = np.linspace(0, 1, num_samples, endpoint=False)
    cosine_ramp = 0.5 * (1 - np.cos(2 * np.pi * t))

    # Apply the cosine ramp to the audio segment at the beginning
    audio_segment = audio_segment.overlay(AudioSegment.silent(duration=num_samples), position=0)
    audio_segment = audio_segment.overlay(AudioSegment.silent(duration=num_samples), position=len(audio_segment) - num_samples)
    return audio_segment


panned_audio_matchedleft1 = apply_cosine_ramp(panned_audio_matchedleft1)
panned_audio_mismatchleft1 = apply_cosine_ramp(panned_audio_mismatchleft1)
panned_audio_matchedright1 = apply_cosine_ramp(panned_audio_matchedright1)
panned_audio_mismatchright1 = apply_cosine_ramp(panned_audio_mismatchright1)

panned_audio_matchedright2 = apply_cosine_ramp(panned_audio_matchedright2)
panned_audio_mismatchright2 = apply_cosine_ramp(panned_audio_mismatchright2)
panned_audio_matchedleft2 = apply_cosine_ramp(panned_audio_matchedleft2)
panned_audio_mismatchleft2 = apply_cosine_ramp(panned_audio_mismatchleft2)

# Export the modified audio segments
panned_audio_matchedleft1.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Chairs_F1_matchedleft_ramped.wav", format="wav")
panned_audio_mismatchleft1.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Chairs_F1_mismatchedleft_ramped.wav", format="wav")
panned_audio_matchedright1.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Chairs_F1_matchedright_ramped.wav", format="wav")
panned_audio_mismatchright1.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Chairs_F1_mismatchedright_ramped.wav", format="wav")

panned_audio_matchedright2.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Houses_F2_matchedright_ramped.wav", format="wav")
panned_audio_mismatchright2.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Houses_F2_mismatchedright_ramped.wav", format="wav")
panned_audio_matchedleft2.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Houses_F2_matchedleft_ramped.wav", format="wav")
panned_audio_mismatchleft2.export("C:/Users/maana/Documents/GitHub/TalkingHeads/stim/Audio Cue/Houses_F2_mismatchedleft_ramped.wav", format="wav")