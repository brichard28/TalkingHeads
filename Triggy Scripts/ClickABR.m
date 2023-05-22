%%Now compatible with RME **STILL NEEDS MAJOR REVISION, BUT IS SUITABLE FOR
% FIRST-PASS PILOT**

%ClickABR.m 
% clcall;
 
ear = 3; % 3=dichotic presentation
rate = 7; % click presentation rate (clicks/sec)
N = 2000; % number of desired trials (both polarities)
 
todayStr = datestr(now,'yyyymmdd');
inputInfo=inputdlg({'subject ID: '});
sID = inputInfo{1};

tic;
% params = abr_tests(ear,rate,N);
params = abr_tests_Triggy(ear,rate,N);
save(['matFiles/', todayStr '_' sID '_ClickABRparams.mat'],'params');
t=toc;
fprintf('Experiment complete. Total time elapsed %d min %d sec.\n',floor(t/60),floor(mod(t,60)));