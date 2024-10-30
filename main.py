from dotenv import load_dotenv
import os
import json
from service.audio_service import AudioProcessing
from service.transcription_service import Transcription
from service.text_generation import TextToSpeech
from service.video_service import VideoProcessing
from config.config import settings


def process_video(video_path):
    """Pipeline to process a video with transcription, filler removal, and audio alignment."""

    output_video_path = "./resources/output_with_corrected_audio.mp4"

    # Step 1: Extract audio from video
    # audio_path = AudioProcessing.extract_audio_from_video(video_path)

    # Step 2: Transcribe audio and remove filler words
    transcription_service = Transcription()

    # words_with_timestamps = transcription_service.transcribe_audio_with_timestamps(audio_path)
    with open("./resources/transcription.json", "r") as file:
        words_with_timestamps = json.load(file)

    # filtered_words = transcription_service.remove_filler_words(words_with_timestamps)

    # Step 3: Generate aligned audio
    tts_service = TextToSpeech()
    # print(words_with_timestamps)
    processed_audio_path = tts_service.generate_aligned_audio(words_with_timestamps)

    # Step 4: Merge processed audio with the video
    VideoProcessing.merge_audio_with_video(video_path, processed_audio_path, output_video_path)
    print("Processed video saved at:", output_video_path)


if __name__ == "__main__":
    process_video(settings.INPUT_VIDEO_PATH)
