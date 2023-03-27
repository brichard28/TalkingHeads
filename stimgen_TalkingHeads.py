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

SubID=input("Enter subject id:")
trials= 10

all_sentences_F1 = [];
all_sentences_F2 = [];

for itrial in range(trials):

    # Defining sentence Variables 
    Name= ["Allen","Doris","Kathy","Lucy","Nina","Peter","Rachel","Steven","Thomas","William"]
    Verb= ["bought","gives","got","has","kept","ordered","prefers","sees","sold","wants"]
    number=["nineteen","seven","fifteen","four","seven","sixty","three","eight","twelve","four","two","nine"]
    adjective=["large","pretty","small","green","cheap","old","red","heavy","white","dark"]
    plural= ["chairs","sofas","desks","tables","flowers","toys","spoons","windows","houses","rings"]
    num=["_1"]
    ext=[".mp4"]
    
    # Finding if Sentence 1 is in the directory
    l=[Name,Verb,number,adjective,plural]
    print(l)
    l2=[num,ext]
    print(l2)
    path= "C:\\Users\\benri\\Documents\\PhD Year 2\\Maanasa Mentorship\\stim\\Structured Sentences F1_MP4"
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
    path2= "C:\\Users\\benri\\Documents\\PhD Year 2\\Maanasa Mentorship\\stim\\Structured Sentences F2_MP4"
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
    
    
    
    
    # Generating Videos
    base_dir = "C:\\Users\\benri\\Documents\\PhD Year 2\\Maanasa Mentorship\\stim\\Structured Sentences F1_MP4"
    base_dir2 = "C:\\Users\\benri\\Documents\\PhD Year 2\\Maanasa Mentorship\\stim\\Structured Sentences F2_MP4"
    cl1= VideoFileClip(os.path.join(base_dir,sentence1))
    cl2= VideoFileClip(os.path.join(base_dir2,sentence2))

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
    duration1= cl1.duration
    
    clip1= cl1; #.subclip(0,duration1)
    #d2= cl2.set_duration(3)
    #duration2= cl2.duration
    clip2= cl2; #cl2.subclip(0,duration2)
    combined=clips_array([[clip1,clip2]])
    combined.write_videofile("C:\\Users\\benri\\Documents\\GitHub\\TalkingHeads\\stim\\" + SubID + "trial_" + str(itrial) + ".mp4")


pandas.DataFrame(all_sentences_F1).to_csv("C:\\Users\\benri\\Documents\\GitHub\\TalkingHeads\\stim\\" + SubID + "all_sentences_F1.csv")
pandas.DataFrame(all_sentences_F2).to_csv("C:\\Users\\benri\\Documents\\GitHub\\TalkingHeads\\stim\\" + SubID + "all_sentences_F2.csv")
