import os
import json
import requests
from google.cloud import speech
from config.config import settings
from service.audio_service import AudioProcessing
from tqdm import tqdm  


class Transcription:
    def __init__(self):
        self.client = speech.SpeechClient()

    def transcribe_audio_with_timestamps(self, audio_path):
        """Transcribes audio with timestamps for each word using Google Cloud Speech-to-Text, displaying a progress bar."""
        chunks = AudioProcessing.split_audio_into_chunks(audio_path)
        total_chunks = len(chunks)
        words_with_timestamps = []

        offset = 0
        with tqdm(total=total_chunks, desc="Transcribing audio", unit="chunk") as progress_bar:
            for i, chunk in enumerate(chunks):
                # Save each chunk temporarily for API processing
                chunk_path = f"temp_chunk_{i}.wav"
                chunk.export(chunk_path, format="wav")

                with open(chunk_path, "rb") as audio_file:
                    content = audio_file.read()
                audio = speech.RecognitionAudio(content=content)
                config = speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                    language_code="en-US",
                    enable_word_time_offsets=True,
                )

                response = self.client.recognize(config=config, audio=audio)

                for result in response.results:
                    for word_info in result.alternatives[0].words:
                        words_with_timestamps.append({
                            "word": word_info.word,
                            "start": word_info.start_time.total_seconds() + offset,
                            "end": word_info.end_time.total_seconds() + offset
                        })

                # Update offset time and remove the temporary chunk file
                offset += chunk.duration_seconds
                os.remove(chunk_path)

                # Update progress bar
                progress_bar.update(1)

        # Save transcription with timestamps to JSON
        with open("./resources/transcription.json", "w") as json_file:
            json.dump(words_with_timestamps, json_file, indent=4)

        return words_with_timestamps
    
    def remove_filler_words(self, transcription_text):
        """Removes filler words from transcription text."""
        endpoint = settings.OPENAI_ENDPOINT
        headers = {
            "Content-Type": "application/json",
            "api-key": settings.OPENAI_API_KEY
        }

        # Compose the API request payload
        prompt = f"""
        Please edit the following transcription by removing filler words (e.g., "um," "uh," "like") and correcting any grammatical errors while preserving the overall structure of the sentences as they appear in the original transcription. Additionally:
        
        1. Retain the phrasing and original intent of each sentence without rephrasing unless necessary for clarity.
        2. If the removal of words affects the natural timing, specify the necessary pauses or timing adjustments to maintain a smooth and fluent flow.
        3. Ensure that the final output is clean and polished, but still sounds like natural spoken language.
        
        Original transcription:
        "{transcription_text}"
        """
        data = {
            "messages": [
                {"role": "user", "content": prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.2
            }

        response = requests.post(endpoint, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            filtered_text = result['choices'][0]['message']['content']

            with open("./resources/corrected_transcription.json", "w") as json_file:
                json.dump(filtered_text, json_file, indent=4)

            return filtered_text.strip()
        else:
            raise Exception(f"Error in Azure OpenAI API call: {response.status_code}, {response.text}")
