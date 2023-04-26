import pandas

SubID = input('Enter Subject ID: ')
conditions=pandas.read_csv("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "all_conditions.csv")
conditions = conditions['0']
right_answer= pandas.read_csv("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\stim\\s_" + SubID + "\\" + SubID + "Answerkey.csv")
right_answer= right_answer.iloc[:,1:6].values.tolist()
responses=pandas.read_csv("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\Output\\s_" + SubID + "\\" + SubID + "all_responses.csv")
responses=responses.iloc[:,1:6].values.tolist()

overall_score = []
mr_responses=[]
mr_ak=[]
mr_score=[]
ml_responses=[]
ml_ak=[]
ml_score=[]
mmr_responses=[]
mmr_ak=[]
mmr_score=[]
mml_responses=[]
mml_ak=[]
mml_score=[]


for i1 in range(len(conditions)):
    
    if conditions[i1]=='match right':
        a=responses[i1]
        b=right_answer[i1]
        mr_responses.append(a)
        mr_ak.append(b)
        
    elif conditions[i1]=='match left':
        a=responses[i1]
        b=right_answer[i1]
        ml_responses.append(a)
        ml_ak.append(b)
        
    elif conditions[i1]=='mismatch right':
        a=responses[i1]
        b=right_answer[i1]
        mmr_responses.append(a)
        mmr_ak.append(b)
        
    elif conditions[i1]=='mismatch left':
        a=responses[i1]
        b=right_answer[i1]
        mml_responses.append(a)
        mml_ak.append(b)
  
#Correct % in matched right

for i in range(len(mr_responses)):
    row_correct=0
    for j in range(len(mr_responses[i])):
        if mr_responses[i][j]== mr_ak[i][j]:
            row_correct+=1
    mr_score.append(row_correct)    
avgmr= sum(mr_score)/len(mr_score)    
avgmr_percent= (avgmr/5)*100         
      
# Correct % in matched left
for i in range(len(ml_responses)):
    row_correct=0
    for j in range(len(ml_responses[i])):
        if ml_responses[i][j]== ml_ak[i][j]:
            row_correct+=1
    ml_score.append(row_correct)    
avgml= sum(ml_score)/len(ml_score)    
avgml_percent= (avgml/5)*100 

#Correct % in mismatched right
for i in range(len(mmr_responses)):
    row_correct=0
    for j in range(len(mmr_responses[i])):
        if mmr_responses[i][j]== mmr_ak[i][j]:
            row_correct+=1
    mmr_score.append(row_correct)    
avgmmr= sum(mmr_score)/len(mmr_score)    
avgmmr_percent= (avgmmr/5)*100 

#Correct % in mismatched right
for i in range(len(mml_responses)):
    row_correct=0
    for j in range(len(mml_responses[i])):
        if mml_responses[i][j]== mml_ak[i][j]:
            row_correct+=1
    mml_score.append(row_correct)    
avgmml= sum(mml_score)/len(mml_score)    
avgmml_percent= (avgmml/5)*100 

# Overall Correct %
for i in range(len(right_answer)):
    same_elements = 0
    for j in range(len(right_answer[i])):
        if right_answer[i][j] == responses[i][j]:
            same_elements += 1
    overall_score.append(same_elements)
   
avg= sum(overall_score)/len(overall_score)    
avg_percent= (avg/5)*100 