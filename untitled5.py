# -*- coding: utf-8 -*-
"""
Created on Wed May 17 21:57:11 2023

@author: maana
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
if not os.path.exists("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\stim\\s_" + SubID):
    os.mkdir("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\stim\\s_" + SubID)
    
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

np.random.shuffle(condition_array)

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
    path= "C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\stim\\Structured Sentences F1_MP4"
    obj=os.listdir(path)
    obj1= str(obj)
    num_tries = 0
    while num_tries <= 499:
        l1= ' '.join([random.choice(i) for i in l])
        l3= ''.join([random.choice(i) for i in l2])
        l4=l1+l3
        ind= obj1.find(l4)
        num_tries += 1
        if ind>-1:
            sentence1=l4
            print(sentence1)
            all_sentences_F1.append(sentence1)
            break

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
    path2= "C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\stim\\Structured Sentences F2_MP4"
    obj0=os.listdir(path2)
    obj2= str(obj0)
    L=[Name,Verb,number,adjective,plural]
    num_tries = 0
    while num_tries <= 499:
        L1= ' '.join([random.choice(i) for i in L])
        L2= ''.join([random.choice(i) for i in l2])
        L3=L1+L2
        ind1= obj2.find(L3)
        num_tries += 1
        if ind1>-1:
            sentence2=L3
            print(sentence2)
            all_sentences_F2.append(sentence2)

            break
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