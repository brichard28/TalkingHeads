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



num_trials= 8




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
# Defining sentence Variables 
Name= ['Allen','Doris','Kathy','Lucy','Nina','Peter','Rachel','Steven','Thomas','William']
Verb= ["bought","gives","got","has","kept","ordered","prefers","sees","sold","wants"]
number=["eight","fifteen","four","nine","nineteen","seven","sixty","three","twelve","two"]
adjective=["cheap","dark","green","heavy","large","old","pretty","red","small","white"]
plural= ["chairs","desks","flowers","houses","rings","sofas","spoons","tables","toys","windows"]
Name1= ['Allen','Doris','Kathy','Lucy','Nina','Peter','Rachel','Steven','Thomas','William']
Verb1= ["bought","gives","got","has","kept","ordered","prefers","sees","sold","wants"]
number1=["eight","fifteen","four","nine","nineteen","seven","sixty","three","twelve","two"]
adjective1=["cheap","dark","green","heavy","large","old","pretty","red","small","white"]
plural1= ["chairs","desks","flowers","houses","rings","sofas","spoons","tables","toys","windows"]
num=["_1"]
ext=[".mp4"]
   

for itrial in range(num_trials):
    
    condition_this_trial = condition_array[itrial]
   

  
    
    # Finding if Sentence 1 is in the directory
    l=[Name,Verb,number,adjective,plural]
    print(l)
    l2=[num,ext]
    print(l2)
    path= "C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\stim\\Structured Sentences F1_MP4"
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
   # Name1=Name
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
      # Converting string to list to split extension 
   