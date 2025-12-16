import json
import requests
from typing import Dict, Any

from config import VIA_URL

def run_via_inference_stream(body: Dict[str, Any]) -> str:
    """
    Run a streaming inference request against VIA and return final content.
    """
    final_text = ""

    resp = requests.post(
        f"{VIA_URL}/summarize",
        headers={"Content-Type": "application/json"},
        data=json.dumps(body),
        stream=True,
        timeout=600,
    )
    resp.raise_for_status()

    for raw in resp.iter_lines():
        if not raw:
            continue

        line = raw.strip()
        if not line.startswith(b"data: "):
            continue

        payload_raw = line[len(b"data: "):].decode().strip()
        if payload_raw == "[DONE]":
            break

        try:
            payload = json.loads(payload_raw)
            final_text = payload["choices"][0]["message"]["content"]
        except Exception:
            continue

    return final_text or "(no content)"
