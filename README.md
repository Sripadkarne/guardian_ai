# Guardian AI


Guardian AI is a reference implementation of a multi-video, agentic video analysis system built for GPU-accelerated environments. It demonstrates how to ingest video, run multimodal reasoning on it, and surface both high-level summaries and time-localized events with visual evidence.

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

That service is responsible for:
- Hosting the actual vision-language model
- Performing GPU-accelerated inference
- Streaming results back to the app

The Streamlit app acts as a client and orchestration layer only.

---

## Requirements

- Python 3.10+
- A running inference service that exposes:
  - `POST /files` for video upload
  - `POST /summarize` for multimodal inference (streaming)
- MoviePy requires ```ffpmeg``` to be installed on the system. 

Optional:
- NVIDIA GPU (for acceleration and GPU monitoring)
- `nvidia-smi` available in PATH (for utilization display)
- OpenCV (for live camera capture)

---

## Running the app

1. Start your local inference service on port 8000  
2. Install dependencies
```
pip install -r requirements.txt
```

4. Launch the UI
```
streamlit run app.py
```

## Notes

- The system is model-agnostic at the UI level. Any vision-language model that supports video inputs and streaming responses can be swapped in behind the inference service.
- All model outputs are treated as untrusted and parsed defensively.

---



    
