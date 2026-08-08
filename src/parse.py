import sys
import json

import src.load as load
import src.skill as skill
import src.language as lang
import src.city as city
import src.soft_skill as soft

from pathlib import Path
from typing import TypedDict

class RawOffer(TypedDict):
    job_id: str
    date_captured: str
    company_raw: str
    source: str
    city_raw: str
    raw_text: str

class ParsedOffer(TypedDict):
    job_id: str
    date_captured: str
    company: str
    source: str
    raw_text: str
    city: city.DetectedCity | None
    skills: list[skill.DetectedSkill]
    languages: list[lang.DetectedLang]
    soft_skills: list[soft.DetectedSoftSkill]


def parse_offer(offer: RawOffer, skills_catalog: list[skill.Skill], lang_catalog: list[lang.Lang], soft_skills_catalog: list[soft.SoftSkill], cities_catalog: list[city.City], req_catalog: list[skill.Requirement], level_catalog: list[lang.Level]) -> ParsedOffer:
    detected_skills = skill.detect_skills(offer["raw_text"], skills_catalog, req_catalog)
    detected_soft_skills = soft.detect_soft_skills(offer["raw_text"], soft_skills_catalog)
    detected_languages = lang.detect_languages(offer["raw_text"], lang_catalog, req_catalog, level_catalog)
    detected_city = city.detect_city(offer["city_raw"], cities_catalog)

    return {
        "job_id": offer["job_id"],
        "date_captured": offer["date_captured"],
        "company": offer["company_raw"],
        "source": offer["source"],
        "raw_text": offer["raw_text"],
        "city": detected_city,
        "skills": detected_skills,
        "languages": detected_languages,
        "soft_skills": detected_soft_skills,
    }


def load_catalogs():
    skills_catalog = load.load_skills_catalog()
    lang_catalog = load.load_languages_catalog()
    cities_catalog = load.load_cities_catalog()
    soft_skills_catalog = load.load_soft_skills_catalog()
    req_catalog = load.load_requirements_catalog()
    level_catalog = load.load_levels_catalog()

    return skills_catalog, lang_catalog, req_catalog, level_catalog, cities_catalog, soft_skills_catalog


if __name__ == "__main__":

    offers = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

    offer = offers[0]

    (skills_catalog, lang_catalog, 
    req_catalog, level_catalog, 
    cities_catalog, soft_skills_catalog) = load_catalogs()

    parsed_offer = parse_offer(
    offer,
    skills_catalog,
    lang_catalog,
    soft_skills_catalog,
    cities_catalog,
    req_catalog,
    level_catalog
    )

    Path("offer_parsed.json").write_text(json.dumps(parsed_offer, indent=2, ensure_ascii=False), encoding="utf-8")
