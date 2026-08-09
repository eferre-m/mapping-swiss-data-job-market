import sys
import json

import src.load as load
import src.skill as skill
import src.language as lang
import src.city as city
import src.soft_skill as soft
import src.work_mode as mode
import src.education as education
import src.experience as experience
import src.workload as workload
import src.contract as contract

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
    work_mode: mode.DetectedWorkMode | None
    workload: workload.DetectedWorkload | None
    contract: contract.DetectedContract | None
    education: education.DetectedEducation | None
    experience: experience.DetectedExperience | None
    skills: list[skill.DetectedSkill]
    languages: list[lang.DetectedLang]
    soft_skills: list[soft.DetectedSoftSkill]



def parse_offer(offer: RawOffer, skills_catalog: list[skill.Skill],
                lang_catalog: list[lang.Lang], soft_skills_catalog: list[soft.SoftSkill],
                cities_catalog: list[city.City], req_catalog: list[skill.Requirement],
                level_catalog: list[lang.Level], work_modes_catalog: list[mode.WorkMode],
                educations_catalog: list[education.Education], experiences_catalog: list[experience.Experience],
                workloads_catalog: list[workload.Workload], contracts_catalog: list[contract.Contract],
                durations_catalog: list[contract.Duration]
            ) -> ParsedOffer:
    detected_skills = skill.detect_skills(offer["raw_text"], skills_catalog, req_catalog)
    detected_soft_skills = soft.detect_soft_skills(offer["raw_text"], soft_skills_catalog)
    detected_languages = lang.detect_languages(offer["raw_text"], lang_catalog, req_catalog, level_catalog)
    detected_city = city.detect_city(offer["city_raw"], cities_catalog)
    detected_work_mode = mode.detect_work_mode(offer["raw_text"], work_modes_catalog)
    detected_education = education.detect_education(offer["raw_text"], educations_catalog, req_catalog)
    detected_experience = experience.detect_experience(offer["raw_text"], experiences_catalog)
    detected_workload = workload.detect_workload(offer["raw_text"], workloads_catalog)
    detected_contract = contract.detect_contract(offer["raw_text"], contracts_catalog, durations_catalog)


    return {
        "job_id": offer["job_id"],
        "date_captured": offer["date_captured"],
        "company": offer["company_raw"],
        "role": offer["role"],
        "industry_raw": offer["industry_raw"],
        "source": offer["source"],
        "raw_text": offer["raw_text"],
        "city": detected_city,
        "skills": detected_skills,
        "languages": detected_languages,
        "soft_skills": detected_soft_skills,
        "work_mode": detected_work_mode,
        "workload": detected_workload,
        "contract": detected_contract,
        "education": detected_education,
        "experience": detected_experience
    }


def load_catalogs():
    skills_catalog = load.load_skills_catalog()
    lang_catalog = load.load_languages_catalog()
    cities_catalog = load.load_cities_catalog()
    soft_skills_catalog = load.load_soft_skills_catalog()
    req_catalog = load.load_requirements_catalog()
    level_catalog = load.load_levels_catalog()
    work_modes_catalog = load.load_work_modes_catalog()
    educations_catalog = load.load_educations_catalog()
    experiences_catalog = load.load_experiences_catalog()
    workloads_catalog = load.load_workloads_catalog()
    contracts_catalog = load.load_contracts_catalog()
    durations_catalog = load.load_durations_catalog()

    return (
        skills_catalog, lang_catalog,
        req_catalog, level_catalog,
        cities_catalog, soft_skills_catalog,
        work_modes_catalog, educations_catalog,
        experiences_catalog, workloads_catalog,
        contracts_catalog, durations_catalog
    )


if __name__ == "__main__":

    offers = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

    offer = offers[0]

    (skills_catalog, lang_catalog, 
    req_catalog, level_catalog, 
    cities_catalog, soft_skills_catalog,
    work_modes_catalog, educations_catalog,
    experiences_catalog, workloads_catalog,
    contracts_catalog, durations_catalog) = load_catalogs()

    parsed_offer = parse_offer(
    offer, skills_catalog,
    lang_catalog, soft_skills_catalog,
    cities_catalog, req_catalog,
    level_catalog, work_modes_catalog,
    educations_catalog, experiences_catalog,
    workloads_catalog, contracts_catalog, durations_catalog
    )

    Path("offer_parsed.json").write_text(json.dumps(parsed_offer, indent=2, ensure_ascii=False), encoding="utf-8")
