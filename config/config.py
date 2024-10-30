import os
from dotenv import load_dotenv

load_dotenv('.env')

class Settings:
    OPENAI_API_KEY : str = os.getenv('OPENAI_API_KEY')
    OPENAI_ENDPOINT : str  = os.getenv('OPENAI_ENDPOINT')
    CHUNK_DURATION_MS: int = 30000
    INPUT_VIDEO_PATH : str = "./resources/sample_video.mp4"

settings = Settings()
