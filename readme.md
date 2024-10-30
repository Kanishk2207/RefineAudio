
# Video Audio Processor

This project processes a video by extracting its audio, transcribing speech to text, removing filler words, generating aligned audio, and merging it back with the original video. Google Cloud Platform (GCP) Speech-to-Text API and OpenAI API are used for transcription and text processing.

## Table of Contents
- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Environment Configuration](#environment-configuration)
  - [Google Cloud Platform (GCP) Setup](#google-cloud-platform-gcp-setup)
- [Usage](#usage)
- [Directory Structure](#directory-structure)

## Features
- Extracts audio from video files
- Splits audio into manageable chunks for processing
- Uses GCP Speech-to-Text API to transcribe audio with word-level timestamps
- Removes filler words from transcription using OpenAI
- Generates aligned audio based on modified transcription
- Merges processed audio back with the original video

## Setup

### Prerequisites
- **Python 3.7+**
- **Pipenv** (or `requirements.txt` can be generated if Pipenv isn’t available)
  
To install dependencies with Pipenv, run:
```bash
pipenv install
```

To install dependencies with `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Environment Configuration
1. Create a `.env` file in the root directory of your project with the following variables:
    ```plaintext
    OPENAI_API_KEY=<Your OpenAI API Key>
    OPENAI_ENDPOINT=<Your OpenAI API Endpoint>
    GCP_PROJECT_ID=<Your GCP Project ID>
    GOOGLE_APPLICATION_CREDENTIALS=path/to/your/gcp-keyfile.json
    ```

2. **Note**: Ensure the `GOOGLE_APPLICATION_CREDENTIALS` path points to your GCP JSON key file (see [GCP Setup](#google-cloud-platform-gcp-setup)).

### Google Cloud Platform (GCP) Setup

#### Step 1: Create a New Project (if not already done)
1. Go to the [GCP Console](https://console.cloud.google.com/).
2. Click on **Select a project** and then **New Project**.
3. Enter a project name and location, then click **Create**.

#### Step 2: Enable APIs
1. In the GCP Console, navigate to **APIs & Services > Library**.
2. Search for **Cloud Speech-to-Text API** and enable it.
3. (Optional) Search for **Cloud Text-to-Speech API** if text synthesis is also required, and enable it.

#### Step 3: Create a Service Account and Download Credentials
1. Go to **APIs & Services > Credentials**.
2. Click **Create Credentials** > **Service Account**.
3. Fill out the service account name and click **Create and Continue**.
4. Grant **Owner** or **Editor** access to the service account (to manage API access) and click **Continue**.
5. Under the **Actions** column, select **Create Key**. Choose JSON format and download the file.
6. Place the downloaded JSON file in the project directory and update the `GOOGLE_APPLICATION_CREDENTIALS` variable in the `.env` file with its path.

#### Step 4: Install and Initialize the Google Cloud SDK (Optional)
If you haven't set up `gcloud` CLI for managing GCP projects:
```bash
# Install gcloud SDK
curl https://sdk.cloud.google.com | bash

# Initialize gcloud
gcloud init
```

## Usage

1. **Run the main processing script**:
   The following command processes a video file, applying all steps in sequence and saving the final output with corrected audio:
   ```bash
   python main.py
   ```
   
   Make sure to place your input video in `./resources/` or specify the correct path in `main.py` under `process_video` function.

2. **Progress Tracking**:
   - While transcribing, the terminal displays a progress bar for Speech-to-Text processing. Each chunk of audio processed will update this bar.
   
3. **Output**:
   - The processed video with aligned audio will be saved as `./resources/output_with_corrected_audio.mp4`.
   - Additional outputs:
     - `./resources/extracted_audio.wav`: Extracted audio from video
     - `./resources/transcription.json`: JSON file with transcription and word-level timestamps
     - `./resources/corrected_transcription.json`: JSON with filler words removed
     - `./resources/processed_audio.wav`: Aligned audio based on modified transcription

## Directory Structure

```plaintext
project-root/
├── config/
│   └── settings.py               # Loads environment variables
├── main.py                       # Main script to run the pipeline
├── services/
│   ├── audio_processing.py       # Audio extraction and chunking functions
│   ├── transcription.py          # Transcription and filler word removal
│   ├── text_generation.py        # Text-to-speech aligned audio generation
│   └── video_processing.py       # Video and audio merging functions
├── resources/                    # Directory for input video and output files
│   ├── sample_video.mp4          # Sample input video (optional)
│   ├── extracted_audio.wav       # Extracted audio file
│   ├── transcription.json        # Transcription with timestamps
│   ├── corrected_transcription.json # Corrected transcription JSON
│   ├── processed_audio.wav       # Aligned audio based on corrected transcription
│   └── output_with_corrected_audio.mp4 # Final processed video
├── .env                          # Environment configuration file
├── README.md                     # Project documentation
└── Pipfile                       # Dependencies
```


