from moviepy.editor import *
import numpy as np
import sounddevice as sd

video = VideoFileClip("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\stim\\s_trig4\\trig4_trial_0_cond_ match left.mp4")
audio = video.audio

sd.default.device = 'ASIO Fireface USB'
sd.play(audio,video.fps,mapping=[1,2,3,4,5])

sd.stop()