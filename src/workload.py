import re

from typing import TypedDict

class Workload(TypedDict):
    workload_id: str
    canonical_name: str
    pattern: re.Pattern

class DetectedWorkload(TypedDict):
    workload_id: str
    canonical_name: str
    

CONTEXT_BEFORE = 50
CONTEXT_AFTER = 50


def detect_presence(text: str, pattern: re.Pattern) -> tuple[bool, str | None]:
    match = pattern.search(text)
    if not match:

        return False, None
    
    start = max(0, match.start() - CONTEXT_BEFORE)
    end = min(len(text), match.end() + CONTEXT_AFTER)

    return True, text[start:end].replace("\n", " ")


def detect_workload(text: str, workloads_catalog: list[Workload]) -> DetectedWorkload | None:
    detected_workload = None

    for workload in workloads_catalog:
        found, _ = detect_presence(text, workload["pattern"])

        if not found:

            return detect_workload

        detected_workload = {
            "workload_id": workload["workload_id"],
            "canonical_name": workload["canonical_name"],
        }
  
    return detected_workload