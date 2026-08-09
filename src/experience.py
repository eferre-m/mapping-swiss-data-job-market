import re

from typing import TypedDict

class Experience(TypedDict):
    experience_id: str
    canonical_name: str
    pattern: re.Pattern

class DetectedExperience(TypedDict):
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


def detect_experience(text: str, experiences_catalog: list[Experience]) -> DetectedExperience | None:
    detected_experience = None

    for experience in experiences_catalog:
        found, _ = detect_presence(text, experience["pattern"])

        if not found:
            continue

        detected_experience = {
            "experience_id": experience["experience_id"],
            "canonical_name": experience["canonical_name"],
        }

    return detected_experience