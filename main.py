import streamlit as st
from dotenv import load_dotenv
import os
import json
from service.audio_service import AudioProcessing
from service.transcription_service import Transcription
from service.text_generation import TextToSpeech
from service.video_service import VideoProcessing
from config.config import settings

# Load environment variables
load_dotenv()

def process_video(video_path):
    """Pipeline to process a video with transcription, filler removal, and audio alignment."""
    output_video_path = "./resources/output_with_corrected_audio.mp4"
    
    audio_path = AudioProcessing.extract_audio_from_video(video_path)
    transcription_service = Transcription()
    
    # Transcribe audio with timestamps
    words_with_timestamps = transcription_service.transcribe_audio_with_timestamps(audio_path)
    with open("./resources/transcription.json", "r") as file:
        words_with_timestamps = json.load(file)
    
    # Remove filler words
    filtered_words = transcription_service.remove_filler_words(words_with_timestamps)
    with open("./resources/corrected_transcription.json", "r") as file:
        corrected_transcription = json.load(file)
    
    # Generate audio aligned with transcription
    tts_service = TextToSpeech()
    processed_audio_path = tts_service.generate_aligned_audio(corrected_transcription)
    
    # Merge audio with video
    VideoProcessing.merge_audio_with_video(video_path, processed_audio_path, output_video_path)
    return output_video_path

# Streamlit UI
st.title("Video Audio Replacement App")
st.write("Upload a video to replace its original audio with AI-generated speech.")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save uploaded file
    input_video_path = f"./resources/{uploaded_file.name}"
    with open(input_video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.write("Processing video...")
    with st.spinner("Transcribing, filtering fillers, and aligning audio..."):
        try:
            output_video_path = process_video(input_video_path)
            st.success("Processing complete!")
            st.video(output_video_path)
            with open(output_video_path, "rb") as f:
                st.download_button("Download Processed Video", f, file_name="output_with_corrected_audio.mp4")
        except Exception as e:
            st.error("An error occurred during processing.")
            st.write(e)
else:
    st.write("Please upload a video file to begin.")
