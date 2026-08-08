import re

from typing import TypedDict

class SoftSkill(TypedDict):
    soft_id: str
    canonical_name: str
    pattern: re.Pattern

class DetectedSoftSkill(TypedDict):
    soft_id: str
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


def detect_soft_skills(text: str, soft_skills_catalog: list[SoftSkill]) -> list[DetectedSoftSkill]:

    detected_soft_skills: list[DetectedSoftSkill] = []

    for soft_skill in soft_skills_catalog:
        found, context = detect_presence(text, soft_skill["pattern"])
        if not found:
            continue
        context
        detected_soft_skills.append(
            {
                "soft_id": soft_skill["soft_id"],
                "canonical_name": soft_skill["canonical_name"],
            }
        )

    return detected_soft_skills