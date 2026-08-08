import re

from typing import TypedDict

class Skill(TypedDict):
    skill_id: str
    canonical_name: str
    pattern: re.Pattern

class Requirement(TypedDict):
    requirement_id: str
    canonical_name: str
    pattern: re.Pattern

class DetectedSkill(TypedDict):
    skill_id: str
    canonical_name: str
    requirement: str
    

CONTEXT_BEFORE = 50
CONTEXT_AFTER = 50


def detect_presence(text: str, pattern: re.Pattern) -> tuple[bool, str | None]:
    match = pattern.search(text)
    if not match:

        return False, None
    
    start = max(0, match.start() - CONTEXT_BEFORE)
    end = min(len(text), match.end() + CONTEXT_AFTER)

    return True, text[start:end].replace("\n", " ")


def detect_requirement(context: str, catalog: list[Requirement]) -> str | None:
    for attribute in catalog:
        if attribute["pattern"].search(context):

            return attribute["requirement_id"]
    
    return None


def detect_skills(text: str, skills_catalog: list[Skill], req_catalog: list[Requirement]) -> list[DetectedSkill]:

    detected_skills: list[DetectedSkill] = []

    for skill in skills_catalog:
        found, context = detect_presence(text, skill["pattern"])
        if not found:
            continue

        requirement = detect_requirement(context, req_catalog)
        detected_skills.append(
            {
                "skill_id": skill["skill_id"],
                "canonical_name": skill["canonical_name"],
                "requirement": requirement,
            }
        )

    return detected_skills