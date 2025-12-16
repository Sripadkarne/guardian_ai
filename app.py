
# app.py

import streamlit as st
import requests

from config import MODEL_NAME
from core.gpu import get_gpu_utilization
from core.via_client import run_via_inference_stream
from core.video_io import (
    save_uploaded_video,
    capture_from_camera,
    extract_event_clips,
)
from core.events import parse_temporal_events

st.set_page_config(page_title="Guardian AI — Dual Stream", layout="wide")
st.title("🎥 Guardian AI — Dual Stream Video Analysis")

# ---------------- GPU ----------------
st.subheader("📈 GPU Monitor")
gpu = get_gpu_utilization()
st.metric("GPU Utilization", f"{gpu:.1f} %" if gpu else "Unavailable")

st.markdown("---")

def init_stream(key: str):
    for field in [
        "file_id", "local_path", "summary", "events", "clips"
    ]:
        st.session_state.setdefault(f"{key}_{field}", None)

def render_stream(key: str, title: str):
    init_stream(key)
    st.subheader(title)

    mode = st.radio("Video source", ["Upload", "Camera"], key=f"{key}_mode")

    if mode == "Upload":
        uploaded = st.file_uploader("Upload video", type=["mp4"], key=key)
        if uploaded:
            path = save_uploaded_video(key, uploaded)
            st.session_state[f"{key}_local_path"] = path
            st.video(path)

            if st.button("Upload to VIA", key=f"{key}_upload"):
                with open(path, "rb") as f:
                    resp = requests.post(
                        "http://localhost:8000/files",
                        data={"purpose": "vision", "media_type": "video"},
                        files={"file": (uploaded.name, f, "video/mp4")},
                    )
                st.session_state[f"{key}_file_id"] = resp.json()["id"]

    else:
        cam = st.selectbox("Camera device", [0, 1], key=f"{key}_cam")
        secs = st.slider("Seconds", 3, 20, 5, key=f"{key}_secs")
        if st.button("Capture", key=f"{key}_cap"):
            path = capture_from_camera(key, cam, secs)
            st.session_state[f"{key}_local_path"] = path
            st.video(path)

    file_id = st.session_state.get(f"{key}_file_id")
    path = st.session_state.get(f"{key}_local_path")

    if not file_id or not path:
        return

    # -------- Summary --------
    st.markdown("### 📝 Summary")
    prompt = st.text_input(
        "Prompt",
        "Summarize the video in 2–3 sentences.",
        key=f"{key}_sum_prompt",
    )

    if st.button("Run Summary", key=f"{key}_sum"):
        body = {
            "id": file_id,
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": True,
            "max_tokens": 256,
        }
        st.session_state[f"{key}_summary"] = run_via_inference_stream(body)

    if st.session_state[f"{key}_summary"]:
        st.success(st.session_state[f"{key}_summary"])

    # -------- Events --------
    st.markdown("### 🚨 Event Detection")
    if st.button("Detect Events", key=f"{key}_events"):
        body = {
            "id": file_id,
            "model": MODEL_NAME,
            "prompt": (
                "Detect dangerous or unusual events.\n"
                "FORMAT ONLY:\n"
                "<start> <end> description"
            ),
            "stream": True,
            "max_tokens": 512,
        }
        text = run_via_inference_stream(body)
        events = parse_temporal_events(text)
        clips = extract_event_clips(key, path, events)

        st.session_state[f"{key}_events"] = events
        st.session_state[f"{key}_clips"] = clips

    if st.session_state[f"{key}_events"]:
        for ev, clip in zip(
            st.session_state[f"{key}_events"],
            st.session_state[f"{key}_clips"],
        ):
            st.write(
                f"**{ev['description']}** ({ev['start']}s → {ev['end']}s)"
            )
            st.video(clip)

# ---------------- Layout ----------------
col1, col2 = st.columns(2)
with col1:
    render_stream("stream1", "📹 Stream 1")
with col2:
    render_stream("stream2", "📹 Stream 2")

st.caption("Guardian AI — Reference Dual-Stream Agentic Video Pipeline")
