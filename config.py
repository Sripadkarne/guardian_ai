import os

VIA_URL = "http://localhost:8000"

VIDEOS_DIR = "videos"
CLIPS_DIR = "clips"

MODEL_NAME = "cosmos-reason1"

os.makedirs(VIDEOS_DIR, exist_ok=True)
os.makedirs(CLIPS_DIR, exist_ok=True)
