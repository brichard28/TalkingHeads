clc;
clear all;
close all;

pilot5Answerkey= readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\stim\s_419_pilot5\419_pilot5Answerkey.csv");
pilot5allresponses =readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\Output\s_419_pilot5\419_pilot5all_responses.csv");
pilot5allconditions = readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\stim\s_419_pilot5\419_pilot5all_conditions.csv");
pilot5allconditions = pilot5allconditions(2:end,2:end);
pilot5allresponses = pilot5allresponses(:,2:end);
pilot5allresponses = pilot5allresponses(2:end,:);
pilot5Answerkey=pilot5Answerkey(:,2:end);
resp5= categorical(table2array(pilot5allresponses));
ak5=categorical(table2array(pilot5Answerkey));
%figure;
%confusionchart(ak5(:),resp5(:))
%title('Pilot5')

pilot4Answerkey= readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\stim\s_419_pilot4\419_pilot4Answerkey.csv");
pilot4allresponses =readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\Output\s_419_pilot4\419_pilot4all_responses.csv");
pilot4allconditions = readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\stim\s_419_pilot4\419_pilot4all_conditions.csv");
pilot4allconditions = pilot4allconditions(2:end,2:end);

pilot4allresponses = pilot4allresponses(:,2:end);
pilot4allresponses = pilot4allresponses(2:end,:);
pilot4Answerkey=pilot4Answerkey(:,2:end);
resp4= categorical(table2array(pilot4allresponses));
ak4=categorical(table2array(pilot4Answerkey));
% figure;
% confusionchart(ak4(:),resp4(:))
% title('Pilot4')

pilot3Answerkey= readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\stim\s_419_pilot3\419_pilot3Answerkey.csv");
pilot3allresponses =readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\Output\s_419_pilot3\419_pilot3all_responses.csv");
pilot3allconditions = readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\stim\s_419_pilot3\419_pilot3all_conditions.csv");
pilot3allconditions = pilot3allconditions(2:end,2:end);

pilot3allresponses = pilot3allresponses(:,2:end);
pilot3allresponses = pilot3allresponses(2:end,:);
pilot3Answerkey=pilot3Answerkey(:,2:end);
resp3= categorical(table2array(pilot3allresponses));
ak3=categorical(table2array(pilot3Answerkey));
% figure;
% confusionchart(ak3(:),resp3(:))
% title('Pilot3')

pilot2Answerkey= readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\stim\s_419_pilot2\419_pilot2Answerkey.csv");
pilot2allresponses =readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\Output\s_419_pilot2\419_pilot2all_responses.csv");
pilot2allconditions = readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\stim\s_419_pilot2\419_pilot2all_conditions.csv");
pilot2allconditions = pilot2allconditions(2:end,2:end);

pilot2allresponses = pilot2allresponses(:,2:end);
pilot2allresponses = pilot2allresponses(2:end,:);
pilot2Answerkey=pilot2Answerkey(:,2:end);
resp2= categorical(table2array(pilot2allresponses));
ak2=categorical(table2array(pilot2Answerkey));
% figure;
% confusionchart(ak2(:),resp2(:))
% title('Pilot2')

pilot002Answerkey= readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\stim\s_pilot002\pilot002Answerkey.csv");
pilot002allresponses =readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\Output\s_pilot002\pilot002all_responses.csv");
pilot002allconditions = readtable("C:\Users\maana\Documents\GitHub\TalkingHeads\stim\s_pilot002\pilot002all_conditions.csv");
pilot002allconditions = pilot002allconditions(2:end,2:end);

pilot002allresponses = pilot002allresponses(:,2:end);
pilot002allresponses = pilot002allresponses(2:end,:);
pilot002Answerkey=pilot002Answerkey(:,2:end);
resp002= categorical(table2array(pilot002allresponses));
ak002=categorical(table2array(pilot002Answerkey));
% figure;
% confusionchart(ak002(:),resp002(:))
% title('Pilot 002')

figure;
confusionchart([ak002(:);ak2(:);ak3(:);ak4(:);ak5(:)],[resp002(:);resp2(:);resp3(:);resp4(:);resp5(:)])
title('All Subjects')

figure;
ak002_mismatch = ak002(categorical(table2array(pilot002allconditions)) == 'mismatch left' | categorical(table2array(pilot002allconditions)) == 'mismatch right',:);
ak2_mismatch = ak2(categorical(table2array(pilot2allconditions)) == 'mismatch left' | categorical(table2array(pilot2allconditions)) == 'mismatch right',:);
ak3_mismatch = ak3(categorical(table2array(pilot3allconditions)) == 'mismatch left' | categorical(table2array(pilot3allconditions)) == 'mismatch right',:);
ak4_mismatch = ak4(categorical(table2array(pilot4allconditions)) == 'mismatch left' | categorical(table2array(pilot4allconditions)) == 'mismatch right',:);
ak5_mismatch = ak5(categorical(table2array(pilot5allconditions)) == 'mismatch left' | categorical(table2array(pilot5allconditions)) == 'mismatch right',:);
resp002_mismatch = resp002(categorical(table2array(pilot002allconditions)) == 'mismatch left' | categorical(table2array(pilot002allconditions)) == 'mismatch right',:);
resp2_mismatch = resp2(categorical(table2array(pilot2allconditions)) == 'mismatch left' | categorical(table2array(pilot2allconditions)) == 'mismatch right',:);
resp3_mismatch = resp3(categorical(table2array(pilot3allconditions)) == 'mismatch left' | categorical(table2array(pilot3allconditions)) == 'mismatch right',:);
resp4_mismatch = resp4(categorical(table2array(pilot4allconditions)) == 'mismatch left' | categorical(table2array(pilot4allconditions)) == 'mismatch right',:);
resp5_mismatch = resp5(categorical(table2array(pilot5allconditions)) == 'mismatch left' | categorical(table2array(pilot5allconditions)) == 'mismatch right',:);

confusionchart([ak002_mismatch(:);ak2_mismatch(:);ak3_mismatch(:);ak4_mismatch(:);ak5_mismatch(:)],[resp002_mismatch(:);resp2_mismatch(:);resp3_mismatch(:);resp4_mismatch(:);resp5_mismatch(:)])
title('Mismatch Trials Only')

figure;
ak002_match = ak002((categorical(table2array(pilot002allconditions)) == 'match left') | (categorical(table2array(pilot002allconditions)) == 'match right'),:);
ak2_match = ak2(categorical(table2array(pilot2allconditions)) == 'match left' | categorical(table2array(pilot2allconditions)) == 'match right',:);
ak3_match = ak3(categorical(table2array(pilot3allconditions)) == 'match left' | categorical(table2array(pilot3allconditions)) == 'match right',:);
ak4_match = ak4(categorical(table2array(pilot4allconditions)) == 'match left' | categorical(table2array(pilot4allconditions)) == 'match right',:);
ak5_match = ak5(categorical(table2array(pilot5allconditions)) == 'match left' | categorical(table2array(pilot5allconditions)) == 'match right',:);
resp002_match = resp002(categorical(table2array(pilot002allconditions)) == 'match left' | categorical(table2array(pilot002allconditions)) == 'match right',:);
resp2_match = resp2(categorical(table2array(pilot2allconditions)) == 'match left' | categorical(table2array(pilot2allconditions)) == 'match right',:);
resp3_match = resp3(categorical(table2array(pilot3allconditions)) == 'match left' | categorical(table2array(pilot3allconditions)) == 'match right',:);
resp4_match = resp4(categorical(table2array(pilot4allconditions)) == 'match left' | categorical(table2array(pilot4allconditions)) == 'match right',:);
resp5_match = resp5(categorical(table2array(pilot5allconditions)) == 'match left' | categorical(table2array(pilot5allconditions)) == 'match right',:);

confusionchart([ak002_match(:);ak2_match(:);ak3_match(:);ak4_match(:);ak5_match(:)],[resp002_match(:);resp2_match(:);resp3_match(:);resp4_match(:);resp5_match(:)])
title('Match Trials Only')