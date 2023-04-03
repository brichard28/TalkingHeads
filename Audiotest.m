[x1,fs1]=audioread("C:\Users\maana\Documents\GitHub\TalkingHeads\stim\Structered Sentences F1_Mp3\Allen bought nineteen large chairs_1.wav")
[x2,fs2]=audioread("C:\Users\maana\Documents\GitHub\TalkingHeads\stim\Structured Sentences F2_Mp3\Doris ordered twelve cheap desks_1.wav")
t1= (0:length(x1)-1)/fs1
t2= (0:length(x2)-1)/fs2
hold on

plot(t1,x1)
%plot(t2,x2)
hold off