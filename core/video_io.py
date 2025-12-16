import os
from typing import List, Dict, Optional

from moviepy.editor import VideoFileClip

try:
    import cv2
except ImportError:
    cv2 = None

from config import VIDEOS_DIR, CLIPS_DIR

def save_uploaded_video(stream_key: str, uploaded) -> str:
    path = os.path.join(VIDEOS_DIR, f"{stream_key}_{uploaded.name}")
    with open(path, "wb") as f:
        f.write(uploaded.getbuffer())
    return path


def capture_from_camera(
    stream_key: str, device_index: int, seconds: int, fps: int = 30
) -> Optional[str]:
    if cv2 is None:
        return None

    cap = cv2.VideoCapture(device_index)
    if not cap.isOpened():
        return None

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)

    out_path = os.path.join(VIDEOS_DIR, f"{stream_key}_camera.mp4")
    out = cv2.VideoWriter(
        out_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    for _ in range(seconds * fps):
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

    return out_path


def extract_event_clips(
    stream_key: str, video_path: str, events: List[Dict]
) -> List[str]:
    clips = []
    base = VideoFileClip(video_path)

    for i, ev in enumerate(events, start=1):
        start = max(0, ev["start"] - 1.0)
        end = min(base.duration, ev["end"] + 1.5)

        out_path = os.path.join(CLIPS_DIR, f"{stream_key}_event_{i}.mp4")
        sub = base.subclip(start, end)
        sub.write_videofile(
            out_path,
            codec="libx264",
            audio=False,
            verbose=False,
            logger=None,
        )
        clips.append(out_path)

    base.close()
    return clips
