import re
from typing import List, Dict

EVENT_PATTERN = re.compile(
    r"<(\d+\.?\d*)>\s*<(\d+\.?\d*)>\s*(.+?)(?=(?:<\d+\.?\d*>\s*<\d+\.?\d*>)|$)",
    re.DOTALL,
)

def parse_temporal_events(text: str) -> List[Dict]:
    """
    Parse model-generated temporal events from strict <start> <end> format.
    """
    events = []

    for match in EVENT_PATTERN.finditer(text):
        try:
            start = float(match.group(1))
            end = float(match.group(2))
            desc = match.group(3).strip()

            if end > start:
                events.append(
                    {"start": start, "end": end, "description": desc}
                )
        except Exception:
            continue

    return events
