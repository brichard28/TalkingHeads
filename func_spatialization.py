import numpy as np
import os
import soundfile as sf
import sounddevice as sd
import random
import time

import matplotlib.pylab as plt
import pdb

from utils import *


def spatialize_seq(seq_dict,ild,itd,fs):
    '''
    This function read each minisequence in seq_dic and apply ild and itd to it and create a new dict with 
    all possible combination of minisequence and ild and itd.

    Note: here we're using broadband ild and itd. For itd, the signal power should be the same as source, 
    however for ild, we're attenuating the far ear to achieve the interaural level difference. 
    To compensate for the lower average energy for ild spatialized condition, I'm attenuating itd condition 
    to make the average rms power for the 2 channels to be the same for ild and itd stimuli. 
    Also, since I'm delaying far ear with itd (~20 samples with long itd), to make sure ild and itd stimuli 
    are of same length, I'm truncating setting the extra samples for the far ear to be 0 and used a 0.01 sec 
    linear ramp for the resulting 

    Input:
    - seq_dict: a dictionary containing all minisequences, with key being condition+idx, e.g. "up-1", "zigzag-4"
    - ild: a scalar in dB
    - itd: a scalar in miscrosec 
    - fs: sampling rate

    Output:
    - seq_dict_ild: spatialized minisequence with ild
    - seq_dict_itd: spatialized minisequence with itd
    '''
    
    seq_dict_ild = dict()
    seq_dict_itd = dict()

    for key in seq_dict:
        key_l = key + '_l'
        key_r = key + '_r'
        sig = seq_dict[key]

        # for ild, attenuate weaker channel
        seq_ild_l = np.concatenate((sig.reshape(-1,1),attenuate_db(sig,ild).reshape(-1,1)),axis=1)
        seq_ild_r = np.concatenate((attenuate_db(sig,ild).reshape(-1,1),sig.reshape(-1,1)),axis=1)

        # for itd, delay further channel
        itd_samps = int(itd * fs)
        seq_itd_l = np.concatenate((np.concatenate((sig,np.zeros(itd_samps))).reshape(-1,1),np.concatenate((np.zeros(itd_samps),sig)).reshape(-1,1)),axis=1)
        seq_itd_r = np.concatenate((np.concatenate((np.zeros(itd_samps),sig)).reshape(-1,1),np.concatenate((sig,np.zeros(itd_samps))).reshape(-1,1)),axis=1)

        # adjust mean RMS (did this before adjust length to avoid effect of extra final ramp)
        mean_rms_ild = np.mean([computeRMS(seq_ild_l[:,0]),computeRMS(seq_ild_l[:,1])])
        mean_rms_itd = np.mean([computeRMS(seq_itd_l[:,0]),computeRMS(seq_itd_l[:,1])])
        seq_itd_l = seq_itd_l*mean_rms_ild/mean_rms_itd
        seq_itd_r = seq_itd_r*mean_rms_ild/mean_rms_itd

        # adjusted length of ILD and ITD spatialized stimuli
        ramp_len = int(0.01*fs)
        trunc_func = np.ones(seq_itd_l.shape)
        trunc_func[-itd_samps:] = 0
        trunc_func[-(itd_samps+ramp_len):-itd_samps] = np.tile(np.linspace(1,0,ramp_len).reshape(-1,1),(1,2)) 
        
        seq_itd_l = seq_itd_l*trunc_func
        seq_itd_r = seq_itd_r*trunc_func
        seq_itd_l = seq_itd_l[:seq_ild_l.shape[0]]
        seq_itd_r = seq_itd_r[:seq_ild_r.shape[0]]

        # add spatialized sequences into new dicts
        seq_dict_ild[key_l] = seq_ild_l
        seq_dict_ild[key_r] = seq_ild_r
        seq_dict_itd[key_l] = seq_itd_l
        seq_dict_itd[key_r] = seq_itd_r

    return seq_dict_ild, seq_dict_itd
    