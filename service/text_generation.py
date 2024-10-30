import os
from google.cloud import texttospeech
from pydub import AudioSegment
from tqdm import tqdm  # Import tqdm for progress bar


class TextToSpeech:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def generate_aligned_audio(self, filtered_words, output_audio_path="./resources/processed_audio.wav"):
        """Generates audio aligned with phrases using Google Cloud Text-to-Speech."""
        # Group words into phrases based on small gaps between them
        phrases = []
        current_phrase = {"words": [], "start": None, "end": None}
        max_gap = 0.2  # Max gap (in seconds) between words to keep them in the same phrase

        for i, word_info in enumerate(filtered_words):
            if current_phrase["start"] is None:
                current_phrase["start"] = word_info["start"]

            # If there is a gap larger than max_gap, start a new phrase
            if i > 0 and word_info["start"] - filtered_words[i - 1]["end"] > max_gap:
                current_phrase["end"] = filtered_words[i - 1]["end"]
                phrases.append(current_phrase)
                current_phrase = {"words": [], "start": word_info["start"], "end": None}

            current_phrase["words"].append(word_info["word"])

        current_phrase["end"] = filtered_words[-1]["end"]
        phrases.append(current_phrase)

        # Initialize an empty audio segment to hold the final aligned audio
        aligned_audio = AudioSegment.silent(duration=0)

        current_position_ms = 0

        # Create a progress bar for processing phrases
        with tqdm(total=len(phrases), desc="Generating aligned audio", unit="phrase") as progress_bar:
            for phrase_info in phrases:
                phrase_text = " ".join(phrase_info["words"])
                phrase_start_ms = int(phrase_info["start"] * 1000)
                phrase_end_ms = int(phrase_info["end"] * 1000)

                # Calculate any silence needed to align the phrase's start time
                if phrase_start_ms > current_position_ms:
                    silence_duration = phrase_start_ms - current_position_ms
                    aligned_audio += AudioSegment.silent(duration=silence_duration)
                    current_position_ms += silence_duration

                synthesis_input = texttospeech.SynthesisInput(text=phrase_text)
                voice = texttospeech.VoiceSelectionParams(language_code="en-us", name="en-US-Journey-F")
                audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

                response = self.client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

                temp_phrase_audio_path = "temp_phrase_audio.wav"
                with open(temp_phrase_audio_path, "wb") as temp_file:
                    temp_file.write(response.audio_content)

                phrase_audio = AudioSegment.from_wav(temp_phrase_audio_path)

                aligned_audio += phrase_audio
                current_position_ms += len(phrase_audio)

                # Calculate any silence needed after the phrase to ensure the next phrase starts correctly
                if current_position_ms < phrase_end_ms:
                    silence_after_phrase = phrase_end_ms - current_position_ms
                    aligned_audio += AudioSegment.silent(duration=silence_after_phrase)
                    current_position_ms += silence_after_phrase

                os.remove(temp_phrase_audio_path)

                # Update progress bar
                progress_bar.update(1)

        aligned_audio.export(output_audio_path, format="wav")
        print(f"Processed audio saved to {output_audio_path}")
        return output_audio_path
