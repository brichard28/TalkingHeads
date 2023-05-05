Answer= readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\stim\s_419_pilot5\419_pilot5Answerkey.csv")
response =readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\Output\s_419_pilot5\419_pilot5all_responses.csv")
c=confusionmat(Answer,response)