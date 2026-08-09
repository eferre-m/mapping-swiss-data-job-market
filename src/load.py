import csv
import re

from pathlib import Path


CATALOG_DIR = Path(__file__).parent.parent / "catalogs"

def load_skills_catalog():
    skills = []
    with open(CATALOG_DIR / "skills.csv", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            skills.append(
                {
                    "skill_id": row["skill_id"],
                    "canonical_name": row["canonical_name"],
                    "pattern": re.compile(row["pattern"], re.I)
                    # TODO: Extend patterns with aliases
                }
            )

    return skills


def load_languages_catalog():
    languages = []
    with open(CATALOG_DIR / "languages.csv", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            languages.append(
                {
                    "lang_id": row["lang_id"],
                    "canonical_name": row["canonical_name"],
                    "pattern": re.compile(row["pattern"], re.I)
                }
            )

    return languages


def load_soft_skills_catalog():
    soft_skills = []
    with open(CATALOG_DIR / "soft_skills.csv", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            soft_skills.append(
                {
                    "soft_id": row["soft_id"],
                    "canonical_name": row["canonical_name"],
                    "pattern": re.compile(row["pattern"], re.I)
                }
            )

    return soft_skills


def load_cities_catalog():
    cities = []
    with open(CATALOG_DIR / "cities.csv", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            cities.append(
                {
                    "city_id": row["city_id"],
                    "canonical_name": row["canonical_name"],
                    "canton": row["canton"],
                    "pattern": re.compile(row["pattern"], re.I)
                }
            )

    return cities


def load_requirements_catalog():
    requirements = []
    with open(CATALOG_DIR / "requirements.csv", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            requirements.append(
                {
                    "requirement_id": row["requirement_id"],
                    "canonical_name": row["canonical_name"],
                    "pattern": re.compile(row["pattern"], re.I)
                }
            )

    return requirements


def load_levels_catalog():
    levels = []
    with open(CATALOG_DIR / "levels.csv", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            levels.append(
                {
                    "level_id": row["level_id"],
                    "canonical_name": row["canonical_name"],
                    "pattern": re.compile(row["pattern"], re.I)
                }
            )

    return levels


def load_work_modes_catalog():
    work_mode = []
    with open(CATALOG_DIR / "work_modes.csv", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            work_mode.append(
                {
                    "work_mode_id": row["work_mode_id"],
                    "canonical_name": row["canonical_name"],
                    "pattern": re.compile(row["pattern"], re.I)
                }
            )

    return work_mode


def load_educations_catalog():
    education = []
    with open(CATALOG_DIR / "educations.csv", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            education.append(
                {
                    "education_id": row["education_id"],
                    "canonical_name": row["canonical_name"],
                    "pattern": re.compile(row["pattern"], re.I)
                }
            )

    return education


def load_experiences_catalog():
    experience = []
    with open(CATALOG_DIR / "experiences.csv", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            experience.append(
                {
                    "experience_id": row["experience_id"],
                    "canonical_name": row["canonical_name"],
                    "pattern": re.compile(row["pattern"], re.I)
                }
            )

    return experience


def load_workloads_catalog():
    workload = []
    with open(CATALOG_DIR / "workloads.csv", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            workload.append(
                {
                    "workload_id": row["workload_id"],
                    "canonical_name": row["canonical_name"],
                    "pattern": re.compile(row["pattern"], re.I)
                }
            )

    return workload


def load_contracts_catalog():
    contract = []
    with open(CATALOG_DIR / "contracts.csv", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            contract.append(
                {
                    "contract_id": row["contract_id"],
                    "canonical_name": row["canonical_name"],
                    "pattern": re.compile(row["pattern"], re.I)
                }
            )

    return contract


def load_durations_catalog():
    duration = []
    with open(CATALOG_DIR / "durations.csv", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            duration.append(
                {
                    "duration_id": row["duration_id"],
                    "canonical_name": row["canonical_name"],
                    "pattern": re.compile(row["pattern"], re.I)
                }
            )

    return duration