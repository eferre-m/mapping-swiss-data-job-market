import re

from typing import TypedDict

class WorkMode(TypedDict):
    work_mode_id: str
    canonical_name: str
    pattern: re.Pattern

class DetectedWorkMode(TypedDict):
    work_mode_id: str
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


def detect_work_mode(text: str, work_modes_catalog: list[WorkMode]) -> DetectedWorkMode | None:

    remote_found = False
    onsite_found = False
    hybrid_found = False

    for work_mode in work_modes_catalog:
        found, _ = detect_presence(text, work_mode["pattern"])

        if not found:
            continue

        if work_mode["work_mode_id"] == "hybrid":
            hybrid_found = True

        elif work_mode["work_mode_id"] == "remote":
            remote_found = True

        elif work_mode["work_mode_id"] == "onsite":
            onsite_found = True

    if hybrid_found or (remote_found and onsite_found):
        return {
            "work_mode_id": "hybrid",
            "canonical_name": "Hybrid",
        }

    if remote_found:
        return {
            "work_mode_id": "remote",
            "canonical_name": "Remote",
        }

    if onsite_found:
        return {
            "work_mode_id": "onsite",
            "canonical_name": "On-site",
        }

    return None