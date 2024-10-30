import os
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from config.config import settings


class AudioProcessing:
    @staticmethod
    def extract_audio_from_video(video_path, output_audio_path="./resources/extracted_audio.wav"):
        """Extracts audio from a video file and saves it as a .wav file."""
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(output_audio_path)
        return output_audio_path

    @staticmethod
    def split_audio_into_chunks(audio_path, chunk_duration=settings.CHUNK_DURATION_MS):
        """Splits an audio file into chunks of a specified duration."""
        audio = AudioSegment.from_wav(audio_path)
        audio = audio.set_channels(1)  # Convert to mono
        chunks = [audio[i:i + chunk_duration] for i in range(0, len(audio), chunk_duration)]
        return chunks
