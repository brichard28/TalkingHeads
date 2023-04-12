%function test21(~,~)
stimpath = 'C:\Users\maana\Documents\GitHub\TalkingHeads\GUI code';

disp("Hello!")
load([stimpath,'\F1 talker.mat'])
numberOfWordColumns = 5;  % Combination of words used by the s
numberOfWordsPerColumn = 10; % Number of options per category
targetColumnIndexList= 1:numberOfWordColumns;
%%
%%  response block
global buttonresponse
buttonresponse = strings(1,5);

titletext = 'Response';
exitbuttontext = 'exit';


% trial_count=1;
% switch trial_count
%     case 1 % New Block
% %         infoText = 'Test';
%          buttonText = {''};
% %         actionButtonText = 'begin';
% %         exitbuttontext = '';
% %         gui2('info',infoText,buttonText,actionButtonText,titletext,[],exitbuttontext);
% 
%         actionButtonText = 'begin';
% %         gui2('trial',infoText,buttonText,[],titletext,[],[]);
%         infoText = 'Listen to the cued talker and answer';
%         gui2('trial',infoText,buttonText,actionButtonText,titletext,[],exitbuttontext);
%         pause(.5)
%     otherwise
%         infoText = ['Listen to the sentence where the first word is '];
%         titletext = ['Block '];
%         buttonText = {''};
%         actionButtonText = 'begin';
%         exitbuttontext = '';
%         gui2('trial',infoText,buttonText,actionButtonText,titletext,[],exitbuttontext);
%         pause(.5)
% end



%% Obtain response
infoText = 'Please select the target words from each column. ';
resp = strings(1,5);
%for Word = 1:length(targetColumnIndexList) % turn into a while loop?
buttontext = txt;

infotext = {'Please respond ',;['Response: ', cellstr(resp) ]};
infotext = {'Please respond'};
actionbuttontext = 'Submit';
%subjectresponse  = gui2('response',infotext,buttontext,actionbuttontext,titletext,exitbuttontext);
% subjectresponse{Word}
gui2('response',infotext,buttontext,actionbuttontext,titletext,exitbuttontext);



resp = buttonresponse;%string(subjectresponse{Word});

% end

% buttonText = {''};
% infotext = resp;
% actionbuttontext = 'BAM';
% 
% gui2('trial',infotext,buttontext,actionbuttontext,titletext,[],exitbuttontext);  % Get responses for the whole sequence
% 
% buttonText = {''};
% infoText = {'End of experiment'};
% actionButtonText = '';
% exitbuttontext = 'Exit';
% exitstate = 'Exit';
% gui2('trial',infoText,buttonText,actionButtonText,titletext,[],exitbuttontext);
% state = 0;
% 
% gui2('exit',infotext,buttonText,actionButtonText,titletext,[],exitbuttontext);
% %end