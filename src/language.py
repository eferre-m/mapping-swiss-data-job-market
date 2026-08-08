import re

from typing import TypedDict

class Lang(TypedDict):
    lang_id: str
    canonical_name: str
    pattern: re.Pattern

class Requirement(TypedDict):
    requirement_id: str
    canonical_name: str
    pattern: re.Pattern

class Level(TypedDict):
    level_id: str
    canonical_name: str
    pattern: re.Pattern

class DetectedLang(TypedDict):
    lang_id: str
    canonical_name: str
    requierement: str
    level: str
    

CONTEXT_BEFORE = 50
CONTEXT_AFTER = 50


def detect_level(context: str, catalog: list[Level]) -> str | None:
    for level in catalog:
        if level["pattern"].search(context):

            return level["level_id"]
    
    return None


def detect_presence(text: str, pattern: re.Pattern) -> tuple[bool, str | None]:
    match = pattern.search(text)
    if not match:

        return False, None
    
    start = max(0, match.start() - CONTEXT_BEFORE)
    end = min(len(text), match.end() + CONTEXT_AFTER)

    return True, text[start:end].replace("\n", " ")


def detect_requirement(context: str, catalog: list[Requirement]) -> str | None:
    for requirement in catalog:
        if requirement["pattern"].search(context):

            return requirement["requirement_id"]
    
    return None


def detect_languages(text: str, lang_catalog: list[Lang], req_catalog: list[Requirement], level_catalog: list[Lang]) -> list[DetectedLang]:

    detected_lang: list[DetectedLang] = []

    for lang in lang_catalog:
        found, context = detect_presence(text, lang["pattern"])
        if not found:
            continue

        requirement = detect_requirement(context, req_catalog)
        level = detect_level(context, level_catalog)
        detected_lang.append(
            {
                "lang_id": lang["lang_id"],
                "canonical_name": lang["canonical_name"],
                "requirement": requirement,
                "level": level,
            }
        )

    return detected_lang