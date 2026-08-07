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


if __name__ == "__main__":
    skills_catalog = load_skills_catalog()
    lang_catalog = load_languages_catalog()
    cities_catalog = load_cities_catalog()
    soft_catalog = load_soft_skills_catalog()
    req_catalog = load_requirements_catalog()