# Guardian AI

# Guardian AI — Dual-Stream Video Analysis

Guardian AI is a reference implementation of a dual-stream, agentic video analysis system built for GPU-accelerated environments. It demonstrates how to ingest video, run multimodal reasoning on it, and surface both high-level summaries and time-localized events with visual evidence.

The project was originally developed as a live system during the NVIDIA & Dell GB10 Hackathon and later refactored into a clean, modular architecture suitable for reuse, extension, and open-source sharing.

---

## What this project does

- Accepts video input from file upload or live camera capture
- Uploads video to a local inference service for multimodal reasoning
- Streams model responses in real time
- Generates short natural-language summaries of video content
- Detects and localizes notable or dangerous events with timestamps
- Extracts and displays short video clips as evidence
- Supports two parallel video streams side by side
- Displays GPU utilization when running on NVIDIA hardware

This is intentionally a **reference system**, not a polished product. The focus is on clarity, structure, and end-to-end flow.

---

## Architecture overview

At a high level, the system is split into four layers:

1. **UI layer (Streamlit)**  
   A lightweight interface for interacting with video streams and viewing results.

2. **Inference client**  
   A small client that sends video-aware prompts to a local Vision-Language inference service and streams responses back.

3. **Media pipeline**  
   Handles video uploads, camera capture, timestamped clip extraction, and file management.

4. **Utilities**  
   GPU monitoring and defensive parsing of model outputs.


## How inference works

This app does **not** run models directly.

Instead, it connects to a **locally running inference service** (referred to as VIA in the code) via HTTP:
```
http://localhost:8000
```

