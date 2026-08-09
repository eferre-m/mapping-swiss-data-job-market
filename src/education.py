import re

from typing import TypedDict

class Education(TypedDict):
    education_id: str
    canonical_name: str
    pattern: re.Pattern

class Requirement(TypedDict):
    requirement_id: str
    canonical_name: str
    pattern: re.Pattern

class DetectedEducation(TypedDict):
    education_id: str
    canonical_name: str
    requirement : str
    

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


def detect_education(text: str, educations_catalog: list[Education], req_catalog: list[Requirement]) -> DetectedEducation | None:

    detected_education = None

    for education in educations_catalog:
        found, context = detect_presence(text, education["pattern"])

        if not found:
            continue

        requirement = detect_requirement(context, req_catalog)
        detected_education = {
            "education_id": education["education_id"],
            "canonical_name": education["canonical_name"],
            "requirement": requirement,
        }

    return detected_education