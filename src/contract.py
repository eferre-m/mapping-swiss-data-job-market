import re

from typing import TypedDict

class Contract(TypedDict):
    contract_id: str
    canonical_name: str
    pattern: re.Pattern

class Duration(TypedDict):
    duration_id: str
    canonical_name: str
    pattern: re.Pattern

class DetectedContract(TypedDict):
    contract_id: str
    canonical_name: str
    duration: str
    

CONTEXT_BEFORE = 50
CONTEXT_AFTER = 50


def detect_presence(text: str, pattern: re.Pattern) -> tuple[bool, str | None]:
    match = pattern.search(text)
    if not match:

        return False, None
    
    start = max(0, match.start() - CONTEXT_BEFORE)
    end = min(len(text), match.end() + CONTEXT_AFTER)

    return True, text[start:end].replace("\n", " ")


def detect_duration(context: str, catalog: list[Duration]) -> str | None:
    for duration in catalog:
        if duration["pattern"].search(context):

            return duration["duration_id"]
    
    return None


def detect_contract(text: str, contracts_catalog: list[Contract], durations_catalog: list[Duration]) -> DetectedContract | None:

    detected_contract = None

    for contract in contracts_catalog:
        found, context = detect_presence(text, contract["pattern"])

        if not found:
            continue
        duration = detect_duration(context, durations_catalog)
        detected_contract = {
            "contract_id": contract["contract_id"],
            "canonical_name": contract["canonical_name"],
            "duration": duration
        }

    return detected_contract