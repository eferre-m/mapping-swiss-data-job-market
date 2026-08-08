import re

from typing import TypedDict

class City(TypedDict):
    city_id: str
    canonical_name: str
    canton: str
    pattern: re.Pattern

class DetectedCity(TypedDict):
    city_id: str
    canonical_name: str
    canton: str

def detect_city(city_raw: str, cities_catalog: list[City]) -> DetectedCity | None:

    detected_city = None

    for city in cities_catalog:
        if city["pattern"].search(city_raw):
            detected_city = {
                    "city_id": city["city_id"],
                    "canonical_name": city["canonical_name"],
                    "canton": city["canton"]
                }

    return detected_city