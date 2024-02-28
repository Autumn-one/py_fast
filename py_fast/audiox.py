import pyaudio
import wave
import threading
import time
import noisereduce as nr
from scipy.io import wavfile
from gtts import gTTS
import os
from typing import Optional

class AudioFile:
    CHUNK = 1024

    def __init__(self, file):
        """ 初始化音频 """
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.p.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            output=True
        )
        self.state = "stopped"
        self.current_frame = 0

    def play(self):
        """播放音频"""

        def play_thread():
            self.state = "playing"
            self.stream.start_stream()
            self.wf.setpos(self.current_frame)
            while self.state == "playing":
                data = self.wf.readframes(self.CHUNK)
                if not data:
                    break
                self.current_frame = self.wf.tell()
                self.stream.write(data)
            self.stream.stop_stream()

        thread = threading.Thread(target=play_thread)
        thread.start()

    def pause(self):
        """ 暂停音频 """
        self.state = "paused"

    def stop(self):
        """ 停止音频 """
        self.state = "stopped"

    def play_from(self, start_time):
        """ 从指定的开始时间播放音频 """
        self.current_frame = start_time * self.wf.getframerate()
        self.play()

    def close(self):
        """在完成后，关闭流"""
        self.stream.close()
        self.p.terminate()


def video_to_audio(video_file_name, audio_file_name):
    """
        根据视频文件提取出音频文件
    """
    video = VideoFileClip(video_file_name)
    audio = video.audio
    audio.write_audiofile(audio_file_name)

def reduce_noise(audio_file):
    # 读取音频文件
    rate, data = wavfile.read(audio_file)

    # 使用noisereduce库降噪
    reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=data)

    # 将降噪后的音频写入到新的文件
    wavfile.write("reduced_noise.wav", rate, reduced_noise)

def text_to_speech(text: str, output_file: str, lang: Optional[str]='zh-cn') -> None:
    """
    文字转语音
    """
    # 使用输入的语言代码创建一个语音合成器，如果没有指定，则默认为中文
    tts = gTTS(text=text, lang=lang)

    # 将生成的语音保存为mp3文件
    tts.save(output_file)

    # 代码暂时不会播放生成的音频文件，如果需要播放可以取消下一行的注释
    # os.system("mpg321 " + output_file)