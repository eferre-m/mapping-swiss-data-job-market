import csv
import re

import src.load as load

from pathlib import Path

CONTEXT_BEFORE = 50
CONTEXT_AFTER = 50


def detect_presence(text, pattern):
    match = pattern.search(text)
    if not match:

        return False, None
    
    start = max(0, match.start() - CONTEXT_BEFORE)
    end = min(len(text), match.end() + CONTEXT_AFTER)

    return True, text[start:end].replace("\n", " ")


def detect_attribute(context, catalog):
    for attribute in catalog:
        if attribute["pattern"].search(context):

            return attribute["attribute_id"]
    
    return None


def detect_skills(text, skills_catalog, req_catalog):

    detected_skills = []

    for skill in skills_catalog:
        found, context = detect_presence(text, skill["pattern"])
        if not found:
            continue

        requirement = detect_attribute(context, req_catalog)
        detected_skills.append(
            {
                "skill_id": skill["skill_id"],
                "canonical_name": skill["canonical_name"],
                "requirement": requirement,
            }
        )

    return detected_skills


def parse_offer():
    """
    Parse a job offer into structured data.
    Input: Raw job offer text.
    Output: A dictionary containing the extracted information.
    """


if __name__ == "__main__":
    skills_catalog = load.load_skills_catalog()
    lang_catalog = load.load_languages_catalog()
    cities_catalog = load.load_cities_catalog()
    soft_catalog = load.load_soft_skills_catalog()
    req_catalog = load.load_requirements_catalog()