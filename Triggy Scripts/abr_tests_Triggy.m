%%Now compatible with RME **STILL NEEDS MAJOR REVISION, BUT IS SUITABLE FOR
% FIRST-PASS PILOT**

function params = abr_tests_Triggy(ear,rate,N)
% function abr_tests(ear,rate,N)
%
% Click ABR experiment: presents N clicks at a given rate N (clicks/second)
% to both ears dichotically (ear=3) or individually (LEFT: ear=1, RIGHT:
% ear=2).  Clicks are presented at three different levels:
%
%   80 and 70 nHL, which is 110 and 100 dB peSPL
%       (see Stapells et al. (1982) JASA 72(1), 74-79.
%
% INPUT VARIABLES
%     ear: which ear clicks are presented (1=left, 2=right, 3=dichotically
%          monaural stimuli have 50 dB SNR masking noise in contralateral
%          ear; dichotically presented clicks are presented in alternating
%          polarity, interleved across ears
%    rate: click presentation rate (clicks/second)
%       N: number of desired presentations per level (default=2000)
%
% STIMULUS AND EVENT TRIGGER INFORMATION
%   The click stimuli are generated using generateClick( ) function.
%   Trigger assigments are:                 [+:compression, -:rarefraction]
%     trg(:,:,1) = [1 4; 3 12];     %70 dBnHL: [left+ right+; left- right-]
%     trg(:,:,2) = [16 48; 64 192]; %80 dBnHL: [left+ right+; left- right-]
%
%   To change the level of the contralateral noise masker, modify
%   generateClick( ) function
%   [Line 47]   noise_dBSPL = 50; % masking noise level (dBSPL)
%
% CALIBRATION VALUES
%   last performed on: 08.06.2019 by TN
%   250-Hz piston-phone, 113.67 dBSPL reads 109 mV RMS
%   1-kHz sine tone, amplitude = 1 yields: 73.4 Hz RMS or 109.64 dB SPL
%     113.67 dBSPL + 20*log10(73.4/109) + mic_sensitivity_offset
%
%   Currently running with unshielded ER-3As with the soft tiptrode tubes.
%   Use of shielded ER-2s with RME failed to produce desired intensity
%   levels without clipping.
%
%   Transmission delay is approximately 0.98304 ms based on
%   'headphone_delay_test.m' run on 2018-Jun-12
%   TBD for new RME 2019 arrangement
%
%
% Original script 2018-Jun-20 by SCB
% Last edit 08.20.2019 TN. Continuing to clean and work out RME kinks

close all;

if nargin<3
    N = 2000;
end

fprintf('Initializing connection to sound card...\n')
Devices=playrec('getDevices');
if isempty(Devices)
    error(sprintf('There are no devices available using the selected host APIs.\nPlease make sure the RME is powered on!')); %#ok<SPERR>
else
    i=1;
    while ~strcmp(Devices(i).name,'ASIO Fireface USB') && i <= length(Devices)
        i=i+1;
    end
end
fs = Devices(i).defaultSampleRate;
playDev = Devices(i).deviceID;
playrec('init',fs,playDev,-1,20,-1);
fprintf('Success! Connected to %s.\n', Devices(i).name);

Triggy = 1;
while Triggy
    trigtype = input('Are you using the Triggy? (y/n)', 's');
    switch trigtype
        case {'Y', 'y', 'Yes', 'yes', 'YES',}
            TrigType = 'Triggy';
            stimchanList=[1,2,3,4,5,6];
            Triggy = 0;
        case {'N', 'n', 'No', 'no', 'NO',}
            TrigType = 'S/PDIF';
            stimchanList=[1,2,14];
            Triggy = 0;
        otherwise
            fprintf(2, 'Unrecognized response! Try again!');
    end
end

click_dBnHL = [80 70]; % click level in dBnHL
clickThr = 30; % click detection threshold (dB peSPL)--from Stapells et al. (1982)
click_peSPL = clickThr + click_dBnHL; % click presentation level (dB peSPL)
max_dBSPL = 107; % maximum dBSPL; calibrated from 250-Hz sine tone, amp = 1 (was 119)
if max_dBSPL<(max(click_dBnHL+clickThr))
    amp = db2mag([0 -10]);
    warning('Adjust headphone amplifier gain! Press any key to continue...');
    pause;
else
    amp = db2mag(click_peSPL - max_dBSPL); % click amplitude (linear scale)
end
dur = 12.8; % stimulus duration (seconds);
PW = 100; % pulse width (microseconds);
jit = 7; % inter-click interval jitter (milliseconds)

% Event trigger assignments [+:condensation, -:rarefraction]
trg(:,:,1) = [1 3; 2 4]; %80 dBnHL: [left+ left-; right+ right-]
trg(:,:,2) = [5 7; 6 8]; %70 dBnHL: [left+ left-; right+ right-]

nClicksPerBlock = length(1:round(fs/rate):round(dur*fs));
nReps = ceil(N/nClicksPerBlock);

k = 0;
% for n = 1:length(click_dBnHL)
for n = 2
    k = k+1;
    
    switch trigtype
        case {'N', 'n', 'No', 'no', 'NO',} % If you're using the S/PDIF box:
            % Generate click stimulus audio and trigger events list
            
            [stim,events,params(k)] = generateFilteredClick(amp(n),rate,dur,trg(:,:,n),fs,PW,jit,ear); %#ok<AGROW>
            trig=zeros(length(stim),1);
            
            for i = 1:length(events)
                trig(events(i,1):events(i,1)+440)=trignum2scalar(events(i,2))*ones(441,1);
            end
            
        case {'Y', 'y', 'Yes', 'yes', 'YES',} % If you're using the Triggy:
            % Generate click stimulus audio and trigger events list
            
            [stim,events,params(k)] = generateClick_Triggy(amp(n),rate,dur,trg(:,:,n),fs,PW,jit,ear); %#ok<AGROW>
            trig=zeros(length(stim),4);
            
            for i = 1:length(events)
                trig(events{i,1}:events{i,1}+440,events{i,2}) = 0.1*ones(441,length(events{i,2}));
            end
    end
    
    for rep = 1:nReps
        fprintf('Block %d, run: %d of %d\n', n, rep, nReps)
        % Load the stimuli and play back; hold up matlab while playing
        pageno = playrec('play',[stim,trig],stimchanList);
        playrec('block',pageno);
        
    end
end
WaitSecs(2);
end



