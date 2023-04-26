# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:16:45 2023

@author: maana
"""
import pandas

conditions=pandas.read_csv("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\stim\\s_419_pilot4\\419_pilot4all_conditions.csv")
conditions = conditions.iloc[:,1].values.tolist()
right_answer= pandas.read_csv("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\stim\\s_419_pilot4\\419_pilot4Answerkey.csv")
right_answer= right_answer.iloc[:,1:6].values.tolist()
responses=pandas.read_csv("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\Output\\s_419_pilot4\\419_pilot4all_responses.csv")
responses=responses.iloc[:,1:6].values.tolist()
score = []
match_right=[]
match_rightscore=[]
match_left=[]
mismatch_right=[]
mismatch_left=[]
same_elements = 0
for i in range(len(right_answer)):
    
    for j in range(len(right_answer[i])):
        if right_answer[i][j] == responses[i][j]:
            same_elements += 1
            score.append(same_elements)

avg= sum(score)/len(score)    
abg_percent= (avg/5)*100      
mright_responses=[]
mright_answer=[]

for i1 in range(len(conditions)):
    
    if conditions[i1]=='match right':
        a=responses[i1]
        match_right.append(a)
       
        
                    
        

                
                
   