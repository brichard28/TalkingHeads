import numpy as np
import os
import soundfile as sf
import sounddevice as sd
import random
import time

import matplotlib.pylab as plt
import pdb


def computeRMS(sig):
    return np.sqrt(np.mean(sig**2))


def attenuate_db(sig,db):
    out = sig * np.exp(np.float32(-db)/8.6860)
    return out


def generate_tone(f_l,f_h,duration,ramp,volume,fs):

    sample_len = int(fs * duration)

    # create samples
    samples_low = (np.sin(2 * np.pi * np.arange(sample_len) * f_l / fs)).astype(np.float32)
    if f_h:
        samples_high =  (np.sin(2 * np.pi * np.arange(sample_len) * f_h / fs)).astype(np.float32)
        samples = samples_low + samples_high
    else:
        samples = samples_low

    # adjust rms
    samples = samples*volume/computeRMS(samples) # np.max(samples)
    
    # add linear ramp
    ramp_len = int(fs * ramp/2)
    ramp_on = np.arange(ramp_len)/ramp_len
    ramp_off = np.flip(ramp_on)
    ramp_samples = np.concatenate((ramp_on,np.ones((sample_len-2*ramp_len)),ramp_off))
    samples = samples * ramp_samples

    #pdb.set_trace()

    return samples

def parse_trial_info(trial_info):

    tone_dur_str = '{}d{}'.format(*str(trial_info["tone_dur"]).split(".")) 
    seq_per_trial_str = str(trial_info["seq_per_trial"]) + "seq"
    isLowLeft_str = "lowLeft" if trial_info["isLowLeft"] else "lowRight"
    isTargetLeft_str = "targetLeft" if trial_info["isTargetLeft"] else "targetRight"
    isTargetPresent_str = "targetTrue" if trial_info["isTargetPresent"] else "targetFalse"
    repeat_loc_str = "repeatloc" + str(trial_info["repeat_loc"])

    if trial_info["isTargetPresent"]:
        trial_info_str = '-'.join([tone_dur_str,seq_per_trial_str,isLowLeft_str,isTargetLeft_str,isTargetPresent_str,repeat_loc_str]) 
    else:
        trial_info_str = '-'.join([tone_dur_str,seq_per_trial_str,isLowLeft_str,isTargetPresent_str]) 

    return trial_info_str


def get_unrepeated_filename(trial_info_str,save_prefix):

    filename = save_prefix + trial_info_str + '.wav'

    if os.path.exists(filename):
        index = 1
        while os.path.exists(f"{filename}_{index}"):
            index += 1
        filename = f"{filename}_{index}"

    return filename