# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 14:30:17 2023

@author: Benjamin Richardson and Maanasa Guru Adimurthy 
"""


#Importing Packages
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
    

num_trials= 48




all_sentences_F1 = [];
all_sentences_F2 = [];

possible_conditions = ["match left","mismatch left","match right","mismatch right"]
# create array of conditions, ensuring there are equal amounts
condition_array = []
for icondition in range(len(possible_conditions)):
    curr_condition = possible_conditions[icondition]
    condition_array_this_condition = []
    for i in range(int(num_trials/len(possible_conditions))):
        condition_array_this_condition.append(curr_condition)
    condition_array.extend(condition_array_this_condition)

np.random.shuffle(condition_array)

for itrial in range(num_trials):
    
    condition_this_trial = condition_array[itrial]

    # Defining sentence Variables 
    Name= ['Allen','Doris','Kathy','Lucy','Nina','Peter','Rachel','Steven','Thomas','William']
    Verb= ["bought","gives","got","has","kept","ordered","prefers","sees","sold","wants"]
    number=["eight","fifteen","four","nine","nineteen","seven","sixty","three","twelve","two"]
    adjective=["cheap","dark","green","heavy","large","old","pretty","red","small","white"]
    plural= ["chairs","desks","flowers","houses","rings","sofas","spoons","tables","toys","windows"]
    num=["_1"]
    ext=[".mp4"]
    
    # Finding if Sentence 1 is in the directory
    l=[Name,Verb,number,adjective,plural]
    print(l)
    l2=[num,ext]
    print(l2)
    path= "D:\\Experiments\\TalkingHeads\\stim\\Structured Sentences F1_MP4"
    obj=os.listdir(path)
    obj1= str(obj)

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
    
    # Remove the words from sentence 1 from originial list 
    Name.remove(name)
    Name1=Name
    print(Name1)
    Verb.remove(verb)
    Verb1=Verb
    print(Verb1)
    number.remove(nu)
    number1=number
    print(number1)
    adjective.remove(ad)
    adjective1=adjective
    print(adjective1)
    plural.remove(pl)
    plural1=plural
    print(plural1)
    
    # Generating Sentence 2
    path2= "D:\\Experiments\\TalkingHeads\\stim\\Structured Sentences F2_MP4"
    obj0=os.listdir(path2)
    obj2= str(obj0)
    L=[Name1,Verb1,number1,adjective1,plural1]
    while True:
        L1= ' '.join([random.choice(i) for i in L])
        L2= ''.join([random.choice(i) for i in l2])
        L3=L1+L2
        ind1= obj2.find(L3)
        if ind1>-1:
            sentence2=L3
            print(sentence2)
            all_sentences_F2.append(sentence2)

            break
    
    
    # Get audio for each sentence
    audio_base_dir = "D:\\Experiments\\TalkingHeads\\stim\\Structured Sentences F1_Mp3"
    audio_base_dir2 = "D:\\Experiments\\TalkingHeads\\stim\\Structured Sentences F2_Mp3"
    fs_1, audio_1 = wavfile.read(os.path.join(audio_base_dir,sentence1.replace(".mp4",".wav")))
    audio_1 =  audio_1*(1/np.max(audio_1))
    fs_2, audio_2 = wavfile.read(os.path.join(audio_base_dir2,sentence2.replace(".mp4",".wav")))
    audio_2 =  audio_2*(1/np.max(audio_2))

    audio1_dict = dict({"audio1":audio_1})
    audio2_dict = dict({"audio2":audio_2})
    audio1_spatialized = spatialize_seq(audio1_dict,0,0.0005,fs_1)
    audio2_spatialized = spatialize_seq(audio2_dict,0,0.0005,fs_2)
    
    if condition_this_trial == 'match left' :
        audio1_spatialized = audio1_spatialized[1]
        audio1_spatialized = audio1_spatialized["audio1_l"]
        rmsset = 0.02;
        rms = np.sqrt(np.mean(audio1_spatialized**2))
        audio1_spatialized = audio1_spatialized * rmsset/rms;
        sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav", audio1_spatialized,fs_1)

        audio2_spatialized = audio2_spatialized[1]
        audio2_spatialized = audio2_spatialized["audio2_r"]
        rmsset = 0.02;
        rms = np.sqrt(np.mean(audio2_spatialized**2))
        audio2_spatialized = audio2_spatialized * rmsset/rms;
        sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav",  audio2_spatialized, fs_2)
    elif  condition_this_trial == 'mismatch left':
            audio1_spatialized = audio1_spatialized[1]
            audio1_spatialized = audio1_spatialized["audio1_r"]
            rmsset = 0.02;
            rms = np.sqrt(np.mean(audio1_spatialized ** 2))
            audio1_spatialized = audio1_spatialized * rmsset / rms;
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav", audio1_spatialized, fs_1)

            audio2_spatialized = audio2_spatialized[1]
            audio2_spatialized = audio2_spatialized["audio2_l"]
            rmsset = 0.02;
            rms = np.sqrt(np.mean(audio2_spatialized ** 2))
            audio2_spatialized = audio2_spatialized * rmsset / rms;
            sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav", audio2_spatialized, fs_2)

    elif condition_this_trial == 'match right':
        audio1_spatialized = audio1_spatialized[1]
        audio1_spatialized = audio1_spatialized["audio1_l"]
        rmsset = 0.02;
        rms = np.sqrt(np.mean(audio1_spatialized**2))
        audio1_spatialized = audio1_spatialized * rmsset/rms;
        sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav", audio1_spatialized, fs_1)

        audio2_spatialized = audio2_spatialized[1]
        audio2_spatialized = audio2_spatialized["audio2_r"]
        rms = np.sqrt(np.mean(audio2_spatialized**2))
        audio2_spatialized = audio2_spatialized * rmsset/rms;
        sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav",  audio2_spatialized, fs_1)
    elif  condition_this_trial == 'mismatch right':
        audio1_spatialized = audio1_spatialized[1]
        audio1_spatialized = audio1_spatialized["audio1_r"]
        rmsset = 0.02;
        rms = np.sqrt(np.mean(audio1_spatialized**2))
        audio1_spatialized = audio1_spatialized * rmsset/rms;
        sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav", audio1_spatialized, fs_1)

        audio2_spatialized = audio2_spatialized[1]
        audio2_spatialized = audio2_spatialized["audio2_l"]
        rms = np.sqrt(np.mean(audio2_spatialized**2))
        audio2_spatialized = audio2_spatialized * rmsset/rms;
        sf.write("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav",  audio2_spatialized, fs_1)
       
    # Generating Videos
    base_dir = "D:\\Experiments\\TalkingHeads\\stim\\Structured Sentences F1_MP4"
    base_dir2 = "D:\\Experiments\\TalkingHeads\\stim\\Structured Sentences F2_MP4"
    
    num=random.randint(0,1)
    
    if num==0:
        cl1= VideoFileClip(os.path.join(base_dir,sentence1))
        audioclip = AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav")
        cl1 = cl1.set_audio(audioclip)
        
        cl2= VideoFileClip(os.path.join(base_dir2,sentence2))
        audioclip = AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav")
        cl2 = cl2.set_audio(audioclip)
    elif num==1:
        cl1= VideoFileClip(os.path.join(base_dir2,sentence2))
        audioclip = AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\sentence_2_spatialized.wav")
        cl1 = cl1.set_audio(audioclip)
        
        cl2= VideoFileClip(os.path.join(base_dir,sentence1))
        audioclip = AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\sentence_1_spatialized.wav")
        cl2 = cl2.set_audio(audioclip)
        
        
    

    raw_duration_clip_1 = cl1.duration
    raw_duration_clip_2 = cl2.duration
    
    longer_duration = np.maximum(raw_duration_clip_1,raw_duration_clip_2)
    
    if raw_duration_clip_1 > raw_duration_clip_2: # if clip 1 is longer
        # get the last frame of clip 2
        last_frame = cl2.get_frame(raw_duration_clip_2)
        extend_video = ImageSequenceClip([last_frame],durations = [raw_duration_clip_1 - raw_duration_clip_2])
        cl2 = concatenate_videoclips([cl2, extend_video])
    elif raw_duration_clip_2 > raw_duration_clip_1:
        last_frame = cl1.get_frame(raw_duration_clip_1)
        extend_video = ImageSequenceClip([last_frame],durations = [raw_duration_clip_2 - raw_duration_clip_1])
        cl1 = concatenate_videoclips([cl1, extend_video])
    #d1=cl1.set_duration(3)
    
    #duration1= cl1.duration
    clip1 = cl1;
    clip2 = cl2;
    combined=clips_array([[clip1,clip2]])
    
       
    if condition_this_trial == 'match right':  
        right_cue = ImageSequenceClip(["right_visual_cue.jpg"], durations = [2])
        right_cue = right_cue.resize(newsize=combined.size)
        if num==0:
            audioclip_right_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Houses_F2_matchedright.wav")
            right_cue= right_cue.set_audio(audioclip_right_match)
            combined_with_cue = CompositeVideoClip([right_cue, # starts at t=0
                                combined.set_start(1)]) # start at t=1s
        
        elif num==1:
            audioclip_right_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Chairs_F1_matchedright.wav")
            right_cue= right_cue.set_audio(audioclip_right_match)
            combined_with_cue = CompositeVideoClip([right_cue, # starts at t=0
                                combined.set_start(1)]) # start at t=1s
    elif condition_this_trial == 'mismatch right':
        right_cue = ImageSequenceClip(["right_visual_cue.jpg"], durations = [2])
        right_cue = right_cue.resize(newsize=combined.size)
        if num==0:
            audioclip_right_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Houses_F2_mismatchedright.wav")
            right_cue= right_cue.set_audio(audioclip_right_match)
            combined_with_cue = CompositeVideoClip([right_cue, # starts at t=0
                                combined.set_start(1)]) # start at t=1s 
        elif num==1:
                audioclip_right_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Chairs_F1_mismatchedright.wav")
                right_cue= right_cue.set_audio(audioclip_right_match)
                combined_with_cue = CompositeVideoClip([right_cue, # starts at t=0
                                    combined.set_start(1)]) # start at t=1s 
            
        
    elif condition_this_trial == 'match left':  
        left_cue = ImageSequenceClip(["left_visual_cue.jpg"], durations = [2])
        left_cue = left_cue.resize(newsize=combined.size)
        if num==0:
            audioclip_left_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Chairs_F1_matchedleft.wav")
            left_cue= left_cue.set_audio(audioclip_left_match)
            combined_with_cue = CompositeVideoClip([left_cue, # starts at t=0
                                combined.set_start(1)]) # start at t=1s
        elif num==1:
            audioclip_left_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Houses_F2_matchedleft.wav")
            left_cue= left_cue.set_audio(audioclip_left_match)
            combined_with_cue = CompositeVideoClip([left_cue, # starts at t=0
                                combined.set_start(1)]) # start at t=1s
            
        
        
    elif condition_this_trial == 'mismatch left':
     left_cue = ImageSequenceClip(["left_visual_cue.jpg"], durations = [2])
     left_cue = left_cue.resize(newsize=combined.size)
     if num==0:
         audioclip_left_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Chairs_F1_mismatchedleft.wav")
         left_cue= left_cue.set_audio(audioclip_left_match)
         combined_with_cue = CompositeVideoClip([left_cue, # starts at t=0
                             combined.set_start(1)]) # start at t=1s
    elif num==1:
        audioclip_left_match=AudioFileClip("D:\\Experiments\\TalkingHeads\\stim\\Audio Cue\\Houses_F2_mismatchedleft.wav")
        left_cue= left_cue.set_audio(audioclip_left_match)
        combined_with_cue = CompositeVideoClip([left_cue, # starts at t=0
                            combined.set_start(1)]) # start at t=1s
         
     
    
    #clip1= cl1; #.subclip(0,duration1)
    #d2= cl2.set_duration(3)
    #duration2= cl2.duration
    #clip2= cl2; #cl2.subclip(0,duration2)
    combined_with_cue.write_videofile("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "_trial_" + str(itrial) + "_cond_ " + str(condition_this_trial) + ".mp4")


pandas.DataFrame(all_sentences_F1).to_csv("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "all_sentences_F1.csv")
pandas.DataFrame(all_sentences_F2).to_csv("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "all_sentences_F2.csv")
pandas.DataFrame(condition_array).to_csv("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "all_conditions.csv")

df1=pandas.read_csv("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "all_conditions.csv")
df2=pandas.read_csv("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "all_sentences_F1.csv")
df3=pandas.read_csv("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "all_sentences_F2.csv")
df1_list= df1["0"].tolist()
df2_list= df2["0"].tolist()
df3_list= df3["0"].tolist()
answerkey=[]
for itrial in range(num_trials):
    a=df1_list[itrial]
    if a== "match left" or a=="mismatch left":
        b=df2_list[itrial]
        answerkey.append(b)
    elif a=="match right" or a=="mismatch right":
        c=df3_list[itrial]
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
    


df = pandas.DataFrame(columns=['Column1', 'Column2','Column3','Column4','Column5'])

for sublist in list_to_string:
    df.loc[len(df)] = sublist

df.to_csv("D:\\Experiments\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "Answerkey.csv")