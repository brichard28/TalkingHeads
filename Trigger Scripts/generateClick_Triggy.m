%
%    Last Edit 09.02.2019
%

function [stim, events, params] = generateClick_Triggy(amp,rate,dur,trg,fs,pulseWidth,jit,ear)
% [stim, events] = generateClick(amp,rate,pulseWidth,jit,maskOtherEar)
%
%   Generates ABR click stimuli in alternating compression and rarefraction
%   polarities.
%
%   INPUT VARIABLES
%                amp : click amplitude (linear scaling)
%               rate : click rate (clicks/second)
%                dur : stimulus duration (seconds)
%                trg : trigger assignments for both polarities <2x2 vector>
%                 fs : TDT sampling frequency (Hz)
%         pulseWidth : click pulse width (microseconds)
%                jit : inter-click interval jitter (milliseconds)
%                ear : present of which ear [1=left, 2=right, 3=dichotic]
%
%   OUTPUT VARIABLE
%               stim : click stimulus audio (2-column vector)
%             events : event triggers [sample#, event#]
%
%   For 'trg' variable
%          rows = polarity [1=pos, 2=neg]
%       columns = ear [1=LEFT, 2=RIGHT]
%
%   An additional two seconds of non-stimulus audio is added to the
%   beginning and end of the the stimulus. In the case of monaurally
%   presented clicks, this non-stimulus audio is masking noise that is
%   slowly ramped on and off for 500 ms (Tukey cosine window). For
%   dichotically presented clicks, two seconds of silence is added. This
%   additional non-stimulus-related time is to accommondate any
%   preprocessing filter responses.f
%
%   The output variables yield a two-column stimulus vector and a
%   two-column event vector that can be used as input variables to the
%   tdt.m class call:
%
%       myTDT.load_stimulus(stim, events);
%
% Assumes usage with ANLTDT 1.6 (Lenny Varghese's TDT class)
% Created: 2018-06-08 SCB
% Last Edit 2019-09-03 TPN

pulse = ones(round(pulseWidth*1e-6*fs),1); % single click "pulse" in samples
ICI = round(fs/rate); % inter-click interval (samples)
stim = zeros(round(dur*fs),2); % pre-populate 'stim' vector
dt = 0.00109;  % RME transmission delay (DAC to eartip in seconds)
%   [measured with oscilloscope on Feb-13-2020]
% Set masking noise parameters
noise_dBSPL = 50; % masking noise level (dBSPL)
noiseAmp = db2mag(noise_dBSPL - 113.67 + 20*log10(1/0.7071)+1.69); % masking noise amplitude

onsets = (1:ICI:length(stim))'; % click onsets for Left Ear (indices)
onsets = cat(2,onsets,round(ICI/2)+onsets); % click onsets for Right Ear (indices)
jitter = round(fs*randi(jit,size(onsets))*1e-3); % add jitter (samples)
onsets = onsets+jitter;
trigonsets = sort(reshape(onsets,[length(onsets)*2,1]));

% Distribute alternating onsets to left and right ears
xt(onsets(1:2:end,1),1) = 1;
xt(onsets(2:2:end,1),1) = -1;

xt(onsets(1:2:end,2),2) = 1;
xt(onsets(2:2:end,2),2) = -1;

% Assign trigger event information [sample# trigger#]
% trgs(1:2:length(onsets),1) = trg(1,1);
% trgs(2:2:length(onsets),1) = trg(1,2);
% trgs(1:2:length(onsets),2) = trg(2,1);
% trgs(2:2:length(onsets),2) = trg(2,2);

trgbin4 = dec2bin(trg);

% If there are only 3 bits, it will throw off the numbering in this
% section. We should have a maximum of 16 for our triggers, so we are
% adding a blank bit to make sure that the counting is correct.
if size(trgbin4,1) < 4
    trgbin4 = [repmat('0',4,1),trgbin4];
end

[trgcol,trgrow] = find(trgbin4=='1');
triggeroutputs = cell(numel(trg),1);

for trigassign = 1:numel(trg)
    triggeroutputs{trigassign} = trgrow(trgcol == trigassign);
end

% trgs(1:4:length(trigonsets),triggeroutputs{1}) = trg(1,1);
% trgs(2:4:length(trigonsets),triggeroutputs{2}) = trg(1,2);
% trgs(3:4:length(trigonsets),triggeroutputs{3}) = trg(2,1);
% trgs(4:4:length(trigonsets),triggeroutputs{4}) = trg(2,2);
trgs = cell(length(trigonsets),1);

trignum = 1;
for cc = 1:length(trigonsets)
    trgs{cc,1} = triggeroutputs{trignum};
    trignum = trignum+1;
    if trignum > 4
        trignum = 1;
    end
end

% Convolve onsets with pulse to create click stimulus 'stim'
stim = amp*cat(2,conv(xt(:,1),pulse),conv(xt(:,2),pulse));
% Zero-pad 1-sec silence at beginning and end
sil = 1; % length of silent gap at beginning and end of stimulus (sec)
stim = cat(1,zeros(round(sil*fs),2),stim,zeros(round(2*fs),2));

events = [num2cell(trigonsets+round((sil+dt)*fs)),trgs];

EAR = {'Left','Right','Alt. Dichotic'};

%% Generate parameters structure
params.stimulus = 'Click Train';
params.amplitude = amp;
params.dBpeSPL = sprintf('%d dBpeSPL',round(113.67+20*log10(amp/0.7071)+1.69));
params.dBnHL = sprintf('%d dBnHL',round(113.67+20*log10(amp/0.7071)+1.69)-30);
params.rate = sprintf('%d/sec',rate);
params.jitter = sprintf('%d milliseconds',jit);
params.pulseWidth = sprintf('%d microseconds',pulseWidth);
params.ear = EAR{ear};
if ear<3
    params.maskingNoise = sprintf('%d dBSPL',noise_dBSPL);
else
    params.maskingNoise = 'N/A';
end
params.numClicks = length(onsets);
params.electrodes = {'1=L mastoid','2=R mastoid',...
    '3=','4=','5=',...
    '6=L tiptrode','7=R tiptrode'};
params.transDelay_ms = 0.98304;
params.date = datestr(now,'yyyymmdd');

end

