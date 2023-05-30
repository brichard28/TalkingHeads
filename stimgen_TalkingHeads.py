# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 14:30:17 2023

@author: Benjamin Richardson and Maanasa Guru Adimurthy 
"""


import random
from random import randint
import os
from moviepy.editor import *
import vlc
import time
import csv
import pandas
import numpy as np
from scipy.io import wavfile
from playsound import playsound
import soundfile as sf
import sounddevice as sd
from func_spatialization import spatialize_seq
from utils import *
import pdb
import numpy.matlib


SubID=input("Enter subject id:")

# make folder if it doesn't exist already
if not os.path.exists("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID):
    os.mkdir("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID)
    



all_sentences_F1 = [];
all_sentences_F2 = [];
num_trials=48
possible_conditions = ["match left","mismatch left","match right","mismatch right"]
# create array of conditions, ensuring there are equal amounts
condition_array = []
for icondition in range(len(possible_conditions)):
    curr_condition = possible_conditions[icondition]
    condition_array_this_condition = []
    for i in range(int(num_trials/len(possible_conditions))):
        condition_array_this_condition.append(curr_condition)
    condition_array.extend(condition_array_this_condition)
#shuffle the condition
np.random.shuffle(condition_array)
#define talker index
talkerindex=[]
# Defining sentence Variables 
Name= ['Allen','Doris','Kathy','Lucy','Nina','Peter','Rachel','Steven','Thomas','William']
Verb= ["bought","gives","got","has","kept","ordered","prefers","sees","sold","wants"]
number=["eight","fifteen","four","nine","nineteen","seven","sixty","three","twelve","two"]
adjective=["cheap","dark","green","heavy","large","old","pretty","red","small","white"]
plural= ["chairs","desks","flowers","houses","rings","sofas","spoons","tables","toys","windows"]
num=["_1"]
ext=[".mp4"]



Name1= ['Allen','Doris','Kathy','Lucy','Nina','Peter','Rachel','Steven','Thomas','William']
Verb1= ["bought","gives","got","has","kept","ordered","prefers","sees","sold","wants"]
number1=["eight","fifteen","four","nine","nineteen","seven","sixty","three","twelve","two"]
adjective1=["cheap","dark","green","heavy","large","old","pretty","red","small","white"]
plural1= ["chairs","desks","flowers","houses","rings","sofas","spoons","tables","toys","windows"]


for itrial in range(num_trials):
    condition_this_trial = condition_array[itrial]
    
    if len(Name)==0:
        Name=Name1.copy()
    if len(Verb)==0:
        Verb=Verb1.copy()
    if len(number)==0:
        number=number1.copy()
    if len(adjective)==0:
        adjective=adjective1.copy()
    if len(plural)==0:
        plural=plural1.copy()
    
    
    # Finding if Sentence 1 is in the directory
    l=[Name,Verb,number,adjective,plural]
    print(l)
    l2=[num,ext]
    print(l2)
    path= "D:\\Experiments\\TalkingHeads\\stim\\Structured Sentences F1_MP4"
    obj=os.listdir(path)
    obj1= str(obj)
    num_tries = 0
    while num_tries <= 499:
        l1= ' '.join([random.choice(i) for i in l])
        l3= ''.join([random.choice(i) for i in l2])
        l4=l1+l3
        ind= obj1.find(l4)
        if ind>-1:
            sentence1=l4
            print(sentence1)
            all_sentences_F1.append(sentence1)
            break
        num_tries += 1


    # If it cannot find a combination with limited words, draw from all words just for this trial, then refill words
    # Do the same for the second sentence later
    if num_tries == 500:
        l=[Name1,Verb1,number1,adjective1,plural1]
        while True:
            l1= ' '.join([random.choice(i) for i in l])
            l3= ''.join([random.choice(i) for i in l2])
            l4=l1+l3
            ind= obj1.find(l4)
            if ind>-1:
                sentence1=l4
                print(sentence1)
                all_sentences_F1.append(sentence1)
                break
        
    # Converting string to list to split extension 
    def Convert(string):
        li=list(string.split("_"))
        return li
    list_to_string= Convert(sentence1)
    
    a= str(list_to_string[0])
    
    def Convert1(string1):
        li1=list(string1.split(" "))
        return li1
    word= Convert1(a)
    print(word)
    name= word[0]
    verb= word[1]
    nu=word[2]
    ad=word[3]
    pl=word[4]
    
    if num_tries != 500:
        # Remove the words from sentence 1 from originial list 
        Name.remove(name)
        #Name1=Name
        #print(Name1)
        Verb.remove(verb)
        #Verb1=Verb
        #print(Verb1)
        number.remove(nu)
        #number1=number
        #print(number1)
        adjective.remove(ad)
        #adjective1=adjective
        #print(adjective1)
        plural.remove(pl)
        #plural1=plural
        #print(plural1)
    
    # Generating Sentence 2
    path2= "D:\\Experiments\\TalkingHeads\\stim\\Structured Sentences F2_MP4"
    obj0=os.listdir(path2)
    obj2= str(obj0)
    L=[Name,Verb,number,adjective,plural]
    num_tries = 0
    while num_tries <= 499:
        L1= ' '.join([random.choice(i) for i in L])
        L2= ''.join([random.choice(i) for i in l2])
        L3=L1+L2
        ind1= obj2.find(L3)
        if ind1>-1:
            sentence2=L3
            print(sentence2)
            all_sentences_F2.append(sentence2)

            break
        num_tries += 1

    # If it cannot find a combination with limited words, draw from all words just for this trial, then refill words
    # Do the same for the second sentence later
    if num_tries == 500:
        l=[Name1,Verb1,number1,adjective1,plural1]
        while True:
            l1= ' '.join([random.choice(i) for i in l])
            l3= ''.join([random.choice(i) for i in l2])
            l4=l1+l3
            ind= obj2.find(l4)
            if ind>-1:
                sentence2=l4
                print(sentence2)
                all_sentences_F2.append(sentence2)
                break
       
    
    list_to_string1= Convert(sentence2)
    
    b= str(list_to_string1[0])
    word1= Convert1(b)
    name1= word1[0]
    verb1= word1[1]
    nu1=word1[2]
    ad1=word1[3]
    pl1=word1[4]
    
    if num_tries != 500:
        Name.remove(name1)
        Verb.remove(verb1)
        number.remove(nu1)
        adjective.remove(ad1)
        plural.remove(pl1)
    
    if num_tries == 500:
        Name=Name1.copy()
        Verb=Verb1.copy()
        number=number1.copy()
        adjective=adjective1.copy()
        plural = plural1.copy() 
    print(num_tries)
   
    
    
    
    # Get audio for each sentence
    audio_base_dir = "D:\\Experiments\\TalkingHeads\\stim\\Structured Sentences F1_Mp3" #audio base directory for talker 1
    audio_base_dir2 = "D:\\Experiments\\TalkingHeads\\stim\\Structured Sentences F2_Mp3" # audio base directory for talker 2
    fs_1, audio_1 = wavfile.read(os.path.join(audio_base_dir,sentence1.replace(".mp4",".wav"))) #reading audio for talker 1
    audio_1 =  audio_1*(1/np.max(audio_1)) #normalizing for RMS
    fs_2, audio_2 = wavfile.read(os.path.join(audio_base_dir2,sentence2.replace(".mp4",".wav"))) #reading audio for talker 2
    audio_2 =  audio_2*(1/np.max(audio_2)) #normalizing for RMS

    audio1_dict = dict({"audio1":audio_1}) #Creating dictionaries for audio 1
    audio2_dict = dict({"audio2":audio_2}) #Creating dictionaries for audio 2
    audio1_spatialized = spatialize_seq(audio1_dict,0,0.0005,fs_1) #Spatializing audio to both directions
    audio2_spatialized = spatialize_seq(audio2_dict,0,0.0005,fs_2) #Spatializing audio to both directions
    
   
    
    
    flips=random.randint(0,1) # whether or not to flip talkers
    talkerindex.append(flips) # append to tracking array
    
    
    
    if flips==0:                               # F1 on left and F2 on right
        if condition_this_trial == 'match left' : #match left condition
            audio1_spatialized = audio1_spatialized[1] # indexing in to dictionary
            audio1_spatialized = audio1_spatialized["audio1_l"] #spatializing to the left
            rmsset = 0.02; #seting rms value
            rms = np.sqrt(np.mean(audio1_spatialized**2)) # calculating rms
            audio1_spatialized = audio1_spatialized * rmsset/rms; #normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav", audio1_spatialized,fs_1) #writing audio file to .wav 

            audio2_spatialized = audio2_spatialized[1] # indexing in to dictionary
            audio2_spatialized = audio2_spatialized["audio2_r"] #spatializing to the right
            rmsset = 0.02; #seting rms value
            rms = np.sqrt(np.mean(audio2_spatialized**2)) # calculating rms
            audio2_spatialized = audio2_spatialized * rmsset/rms; #normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav",  audio2_spatialized, fs_2) #writing audio file to .wav
        elif  condition_this_trial == 'mismatch left':  #mismatch left condition
            audio1_spatialized = audio1_spatialized[1] # indexing in to dictionary
            audio1_spatialized = audio1_spatialized["audio1_r"] #spatializing to the right
            rmsset = 0.02; #seting rms value
            rms = np.sqrt(np.mean(audio1_spatialized ** 2)) # calculating rms
            audio1_spatialized = audio1_spatialized * rmsset / rms; #normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav", audio1_spatialized, fs_1) #writing audio file to .wav

            audio2_spatialized = audio2_spatialized[1] # indexing in to dictionary 
            audio2_spatialized = audio2_spatialized["audio2_l"] #spatializing to the left
            rmsset = 0.02; #seting rms value
            rms = np.sqrt(np.mean(audio2_spatialized ** 2)) # calculating rms
            audio2_spatialized = audio2_spatialized * rmsset / rms; #normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav", audio2_spatialized, fs_2) #writing audio file to .wav

        elif condition_this_trial == 'match right': #match right condition
            audio1_spatialized = audio1_spatialized[1] # indexing in to dictionary 
            audio1_spatialized = audio1_spatialized["audio1_l"] #spatializing to the left
            rmsset = 0.02; #seting rms value
            rms = np.sqrt(np.mean(audio1_spatialized**2)) # calculating rms
            audio1_spatialized = audio1_spatialized * rmsset/rms; #normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav", audio1_spatialized, fs_1)#writing audio file to .wav

            audio2_spatialized = audio2_spatialized[1] # indexing in to dictionary 
            audio2_spatialized = audio2_spatialized["audio2_r"] #spatializing to the right
            rms = np.sqrt(np.mean(audio2_spatialized**2))  # calculating rms
            audio2_spatialized = audio2_spatialized * rmsset/rms;#normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav",  audio2_spatialized, fs_1)#writing audio file to .wav
        elif  condition_this_trial == 'mismatch right': #mismatch right condition
            audio1_spatialized = audio1_spatialized[1] # indexing in to dictionary 
            audio1_spatialized = audio1_spatialized["audio1_r"] #spatializing to the right
            rmsset = 0.02; #seting rms value
            rms = np.sqrt(np.mean(audio1_spatialized**2)) # calculating rms
            audio1_spatialized = audio1_spatialized * rmsset/rms; #normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav", audio1_spatialized, fs_1)#writing audio file to .wav

            audio2_spatialized = audio2_spatialized[1] # indexing in to dictionary 
            audio2_spatialized = audio2_spatialized["audio2_l"] #spatializing to the left
            rms = np.sqrt(np.mean(audio2_spatialized**2))# calculating rms
            audio2_spatialized = audio2_spatialized * rmsset/rms; #normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav",  audio2_spatialized, fs_1)#writing audio file to .wav
    
    if flips==1:                     # F2 on left and F1 on right
        if condition_this_trial == 'match left' : #match left 
            audio1_spatialized = audio1_spatialized[1] # indexing in to dictionary 
            audio1_spatialized = audio1_spatialized["audio1_r"] #spatializing to the right
            rmsset = 0.02; #seting rms value
            rms = np.sqrt(np.mean(audio1_spatialized**2)) # calculating rms
            audio1_spatialized = audio1_spatialized * rmsset/rms; #normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav", audio1_spatialized,fs_1) #writing audio file to .wav

            audio2_spatialized = audio2_spatialized[1] # indexing in to dictionary 
            audio2_spatialized = audio2_spatialized["audio2_l"] #spatializing to the left
            rmsset = 0.02; #seting rms value
            rms = np.sqrt(np.mean(audio2_spatialized**2)) # calculating rms
            audio2_spatialized = audio2_spatialized * rmsset/rms; #normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav",  audio2_spatialized, fs_2) #writing audio file to .wav
        elif  condition_this_trial == 'mismatch left': #mismatch left 
            audio1_spatialized = audio1_spatialized[1] # indexing in to dictionary 
            audio1_spatialized = audio1_spatialized["audio1_l"] #spatializing to the left
            rmsset = 0.02; #seting rms value
            rms = np.sqrt(np.mean(audio1_spatialized ** 2)) # calculating rms
            audio1_spatialized = audio1_spatialized * rmsset / rms; # normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav", audio1_spatialized, fs_1) #writing audio file to .wav

            audio2_spatialized = audio2_spatialized[1] # indexing in to dictionary
            audio2_spatialized = audio2_spatialized["audio2_r"] #spatializing to the right
            rmsset = 0.02; #seting rms value
            rms = np.sqrt(np.mean(audio2_spatialized ** 2)) # calculating rms
            audio2_spatialized = audio2_spatialized * rmsset / rms; # normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav", audio2_spatialized, fs_2)#writing audio file to .wav

        elif condition_this_trial == 'match right':   #match right 
            audio1_spatialized = audio1_spatialized[1] # indexing in to dictionary 
            audio1_spatialized = audio1_spatialized["audio1_r"] #spatializing to the right
            rmsset = 0.02; #seting rms value
            rms = np.sqrt(np.mean(audio1_spatialized**2)) # calculating rms
            audio1_spatialized = audio1_spatialized * rmsset/rms;  # normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav", audio1_spatialized, fs_1)#writing audio file to .wav

            audio2_spatialized = audio2_spatialized[1]
            audio2_spatialized = audio2_spatialized["audio2_l"]
            rms = np.sqrt(np.mean(audio2_spatialized**2)) # calculating rms
            audio2_spatialized = audio2_spatialized * rmsset/rms; # normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav",  audio2_spatialized, fs_1)#writing audio file to .wav
        elif  condition_this_trial == 'mismatch right': #mismatch right 
            audio1_spatialized = audio1_spatialized[1]# indexing in to dictionary 
            audio1_spatialized = audio1_spatialized["audio1_l"] #spatializing to the left
            rmsset = 0.02; #seting rms value
            rms = np.sqrt(np.mean(audio1_spatialized**2)) # calculating rms 
            audio1_spatialized = audio1_spatialized * rmsset/rms;# normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav", audio1_spatialized, fs_1)#writing audio file to .wav

            audio2_spatialized = audio2_spatialized[1]# indexing in to dictionary 
            audio2_spatialized = audio2_spatialized["audio2_r"] #spatializing to the right
            rms = np.sqrt(np.mean(audio2_spatialized**2)) # calculating rms
            audio2_spatialized = audio2_spatialized * rmsset/rms; # normalizing audio
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav",  audio2_spatialized, fs_1)#writing audio file to .wav
        
        
   
       
 # Generating Videos
    base_dir = "D:\\Experiments\\TalkingHeads\\stim\\Structured Sentences F1_MP4" #Video Directory for F1 talker
    base_dir2 = "D:\\Experiments\\TalkingHeads\\stim\\Structured Sentences F2_MP4" #Video directory for F2 talker
    
    
    if flips==0:  # F1 on left and F2 on right
        cl1= VideoFileClip(os.path.join(base_dir,sentence1)) #matching sentence for F1 talker in the Directory
        audioclip = AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav") # reading audio clip
        cl1 = cl1.set_audio(audioclip) # seting audio to the video
        
        cl2= VideoFileClip(os.path.join(base_dir2,sentence2)) #matching sentence for F2 talker in the Directory
        audioclip = AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav") # reading audio clip
        cl2 = cl2.set_audio(audioclip) # seting audio to the video
    elif flips==1: # F2 on left and F1 on right
        cl1= VideoFileClip(os.path.join(base_dir2,sentence2)) #matching sentence for F2 talker in the Directory
        audioclip = AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav") # reading audio clip
        cl1 = cl1.set_audio(audioclip) # seting audio to the video
        
        cl2= VideoFileClip(os.path.join(base_dir,sentence1)) #matching sentence for F1 talker in the Directory
        audioclip = AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav") # reading audio clip
        cl2 = cl2.set_audio(audioclip) # seting audio to the video
        
        
    

    raw_duration_clip_1 = cl1.duration # get length of video 
    raw_duration_clip_2 = cl2.duration # get length of video 
    
    longer_duration = np.maximum(raw_duration_clip_1,raw_duration_clip_2) # Finding duration of longer video
    
    if raw_duration_clip_1 > raw_duration_clip_2: # if clip 1 is longer than clip 2
        # get the last frame of clip 2
        last_frame = cl2.get_frame(raw_duration_clip_2)
        extend_video = ImageSequenceClip([last_frame],durations = [raw_duration_clip_1 - raw_duration_clip_2]) #extend video with image frame
        cl2 = concatenate_videoclips([cl2, extend_video]) #concatenate video clips
    elif raw_duration_clip_2 > raw_duration_clip_1: # if clip 2 is longer than clip 1
        last_frame = cl1.get_frame(raw_duration_clip_1) # get the last frame of clip 1
        extend_video = ImageSequenceClip([last_frame],durations = [raw_duration_clip_2 - raw_duration_clip_1]) #extend video with image frame
        cl1 = concatenate_videoclips([cl1, extend_video]) #concatenate video clips
    #d1=cl1.set_duration(3)
    
    #duration1= cl1.duration
    clip1 = cl1;
    clip2 = cl2;
    combined=clips_array([[clip1,clip2]]) # combing clips to array
    
   #Adding visual cues and audio cues    
    if condition_this_trial == 'match right':  
        right_cue = ImageSequenceClip(["right_visual_cue.jpg"], durations = [2])
        right_cue = right_cue.resize(newsize=combined.size)
        if flips==0: # F1 on left and F2 on right
            audioclip_right_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Houses_F2_matchedright.wav")
            right_cue= right_cue.set_audio(audioclip_right_match)
            combined_with_cue = CompositeVideoClip([right_cue, # starts at t=0
                                combined.set_start(1)]) # start at t=1s

            # Now that it's combined....grab the audio from combined_with_cue (should be 2 channel audio)

            # Add triggers to the audio (channels 3-6)

            # set the audio back to combined_with_cue
        
        elif flips==1: # F2 on left and F1 on right
            audioclip_right_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Chairs_F1_matchedright.wav")
            right_cue= right_cue.set_audio(audioclip_right_match)
            combined_with_cue = CompositeVideoClip([right_cue, # starts at t=0
                                combined.set_start(1)]) # start at t=1s
    elif condition_this_trial == 'mismatch right':
        right_cue = ImageSequenceClip(["right_visual_cue.jpg"], durations = [2])
        right_cue = right_cue.resize(newsize=combined.size)
        if flips==0: # F1 on left and F2 on right
            audioclip_right_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Houses_F2_mismatchedright.wav")
            right_cue= right_cue.set_audio(audioclip_right_match)
            combined_with_cue = CompositeVideoClip([right_cue, # starts at t=0
                                combined.set_start(1)]) # start at t=1s 
        elif flips==1: # F2 on left and F1 on right
                audioclip_right_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Chairs_F1_mismatchedright.wav")
                right_cue= right_cue.set_audio(audioclip_right_match)
                combined_with_cue = CompositeVideoClip([right_cue, # starts at t=0
                                    combined.set_start(1)]) # start at t=1s 
            
        
    elif condition_this_trial == 'match left':  
        left_cue = ImageSequenceClip(["left_visual_cue.jpg"], durations = [2])
        left_cue = left_cue.resize(newsize=combined.size)
        if flips==0: # F1 on left and F2 on right
            audioclip_left_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Chairs_F1_matchedleft.wav")
            left_cue= left_cue.set_audio(audioclip_left_match)
            combined_with_cue = CompositeVideoClip([left_cue, # starts at t=0
                                combined.set_start(1)]) # start at t=1s
        elif flips==1: # F2 on left and F1 on right
            audioclip_left_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Houses_F2_matchedleft.wav")
            left_cue= left_cue.set_audio(audioclip_left_match)
            combined_with_cue = CompositeVideoClip([left_cue, # starts at t=0
                                combined.set_start(1)]) # start at t=1s
            
        
        
    elif condition_this_trial == 'mismatch left':
        left_cue = ImageSequenceClip(["left_visual_cue.jpg"], durations = [2])
        left_cue = left_cue.resize(newsize=combined.size)
        if flips==0: # F1 on left and F2 on right
            audioclip_left_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Chairs_F1_mismatchedleft.wav")
            left_cue= left_cue.set_audio(audioclip_left_match)
            combined_with_cue = CompositeVideoClip([left_cue, # starts at t=0
                             combined.set_start(1)]) # start at t=1s
        elif flips==1: # F2 on left and F1 on right
            audioclip_left_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Houses_F2_mismatchedleft.wav")
            left_cue= left_cue.set_audio(audioclip_left_match)
            combined_with_cue = CompositeVideoClip([left_cue, # starts at t=0
                            combined.set_start(1)]) # start at t=1s
         
     
    
    #clip1= cl1; #.subclip(0,duration1)
    #d2= cl2.set_duration(3)
    #duration2= cl2.duration
    #clip2= cl2; #cl2.subclip(0,duration2)
    combined_with_cue.write_videofile("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "_trial_" + str(itrial) + "_cond_ " + str(condition_this_trial) + ".mp4") # Writing the video


pandas.DataFrame(all_sentences_F1).to_csv("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "all_sentences_F1.csv") #  Creating CSv for F1 Sentences
pandas.DataFrame(all_sentences_F2).to_csv("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "all_sentences_F2.csv") #  Creating CSv for F2 Sentences
pandas.DataFrame(condition_array).to_csv("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "all_conditions.csv") #  Creating CSV all conditions

df1=pandas.read_csv("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "all_conditions.csv") #reading all conditions
df2=pandas.read_csv("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "all_sentences_F1.csv") # Reading F1 sentences
df3=pandas.read_csv("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "all_sentences_F2.csv") # Reading F2 sentences
df1_list= df1["0"].tolist() 
df2_list= df2["0"].tolist()
df3_list= df3["0"].tolist()
answerkey=[] # answer key 

for itrial in range(num_trials): # Creating answe key according to condition
    if talkerindex[itrial]==0:
         a=df1_list[itrial]
         if a== "match left" or a=="mismatch left":
             b=df2_list[itrial]
             answerkey.append(b)
         elif a=="match right" or a=="mismatch right":
             c=df3_list[itrial]
             answerkey.append(c)
    elif talkerindex[itrial]==1:
         a=df1_list[itrial]
         if a== "match left" or a=="mismatch left":
             b=df3_list[itrial]
             answerkey.append(b)
         elif a=="match right" or a=="mismatch right":
             c=df2_list[itrial]
             answerkey.append(c)
       
        
def Convert2(string2):
     li=list(string2.split("_"))
     li.pop(1)
     return li
def Convert3(string3):
     li1=list(string3.split(" "))
     return li1
list_to_string=[]      
for i in range(num_trials):
    mystring=''.join(map(str,answerkey[i]))
    sen=Convert2(mystring)
    mystring1=''.join(map(str,sen))
    sen1=Convert3(mystring1)
    
    list_to_string.append(sen1)
    


df = pandas.DataFrame(columns=['Column1', 'Column2','Column3','Column4','Column5']) #Saving

for sublist in list_to_string:
    df.loc[len(df)] = sublist

df.to_csv("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "Answerkey.csv")