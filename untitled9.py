from moviepy.editor import *
import numpy as np
import sounddevice as sd
import vlc

# Import the video as a moviepy object
video = VideoFileClip("D:\\Experiments\\TalkingHeads\\stim\\s_mastertest001\\mastertest001_trial_0_cond_ match left.mp4")

# extract the audio
audio = video.audio
current_audio = audio.to_soundarray()

# add triggers to the audio (should now be 5 channel audio)
trigger_channel_3 = np.zeros(len(current_audio))
trigger_channel_3[0] = 1
# trigger_channel_3[452] = 0
trigger_channel_4 = np.zeros(len(current_audio))
trigger_channel_4[round(2 * audio.fps)] = 1
trigger_channel_5 = np.zeros(len(current_audio))
trigger_channel_5[len(trigger_channel_5) - 1] = 1
current_audio_with_triggers = np.transpose(np.stack(((current_audio[:, 0], current_audio[:, 1], trigger_channel_3, trigger_channel_4, trigger_channel_5))))
print(np.shape(current_audio_with_triggers))

# Set the audio back to the moviepy object
video.set_audio(current_audio_with_triggers)
video.write_videofile("D:\\Experiments\\TalkingHeads\\Stimulii\\testt.mp4")

# Play it in VLC

file= "D:\\Experiments\\TalkingHeads\\Stimulii\\testt.mp4"
media = vlc.Media(os.path.abspath(file))
media_player = vlc.MediaPlayer()
media_player.set_fullscreen(True)

media_player.set_media(media)
media_player.set_position(0.5)

#sd.default.device = 'ASIO Fireface USB'
#sd.play(audio.to_soundarray(),video.fps,mapping=[1,2,3,4,5])

#sd.stop()