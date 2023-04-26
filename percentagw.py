# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 22:08:50 2023

@author: maana
"""

import pandas
SubID = input('Enter Subject ID: ')
conditions=pandas.read_csv("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "all_conditions.csv")
conditions = conditions['0']
right_answer= pandas.read_csv("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "Answerkey.csv")
right_answer= right_answer.iloc[:,1:6].values.tolist()
responses=pandas.read_csv("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\Output\\s_" + SubID + "\\" + SubID + "all_responses.csv")
responses=responses.iloc[:,1:6].values.tolist()
score = []

for i in range(len(right_answer)):
    same_elements = 0
    for j in range(len(right_answer[i])):
        if right_answer[i][j] == responses[i][j]:
            same_elements += 1
    score.append(same_elements)

avg= sum(score)/len(score)    
avg_percent= (avg/5)*100      