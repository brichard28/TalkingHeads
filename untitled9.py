import moviepy
import numpy as np
import sounddevice as sd

video = moviepy.editor.VideoFileClip("C:\\Users\\maana\\Documents\\GitHub\\TalkingHeads\\stim\\s_trig4\\trig4_trial_0_cond_ match left.mp4")
audio = video.audio
audio= audio.set_fps(video.fps)
audio0=audio.to_soundarray()
trigger_channel_3 = np.zeros(len(audio0))
trigger_channel_3[0] = 50
#trigger_channel_3[452] = 0
trigger_channel_4 =np.zeros(len(audio0))
trigger_channel_4[round(2*video.fps)] = 50
trigger_channel_5 = np.zeros(len(audio0))
trigger_channel_5[len(trigger_channel_5)-1] = 50
audio0= np.transpose(np.stack(((audio0[:,0],audio0[:,1],trigger_channel_3,trigger_channel_4,trigger_channel_5))))
print(np.shape(audio0))
video.set_audio(audio)

sd.default.device = 'ASIO Fireface USB'
sd.play(video,video.fps,mapping=[1,2,3,4,5])

sd.stop()