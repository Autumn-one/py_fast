import pyaudio
import wave
import threading
import time


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
