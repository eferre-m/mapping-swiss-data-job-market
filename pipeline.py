"""
pipeline.py — Connects capture (job_capture.html) with analysis (parse.py) and produces
the enriched "dossier" consumed by review.html.

GOLDEN RULE: this script NEVER overwrites data entered by hand in review.html
(corrections, application_status, notes). If a job_id already exists in the dossier,
it's only re-parsed when --reparse is passed explicitly; otherwise it's left as-is
and only match_percent is recomputed against the current profile.json.

Usage:
    python pipeline.py capture.json                  # first run / bring in new offers
    python pipeline.py capture.json --reparse         # re-analyze EVERYTHING (use after editing catalog CSVs)
    python pipeline.py capture.json --dossier other.json --profile other_profile.json
"""
import argparse
import json
from pathlib import Path

import parse

CEFR_ORDER = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6, "Native": 7}

DEFAULT_DOSSIER = "dossier.json"
DEFAULT_PROFILE = "profile.json"


def load_json(path, default):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def save_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def compute_match(entry, profile):
    """Compares what was detected in the offer (with manual corrections applied)
    against profile.json. Weights: level 2 (required) = 2 points, level 1 (nice) = 1 point,
    a mentioned soft skill = 1 point. Only counts what the offer actually asks for."""
    parsed = entry["parsed"]
    corrections = entry.get("corrections", {})
    total_weight = 0
    matched_weight = 0

    corr_skills = corrections.get("skills", {})
    for skill_id, data in parsed["skills"].items():
        found = corr_skills.get(skill_id, data["found"])
        if not found:
            continue
        weight = 2 if data["status"] == 2 else 1
        total_weight += weight
        if profile.get("skills", {}).get(skill_id):
            matched_weight += weight

    # Skills added by hand in review.html that don't exist in skills.csv yet
    for extra in corrections.get("manual_skills", []):
        total_weight += 1
        if profile.get("skills", {}).get(extra.get("id")):
            matched_weight += 1

    corr_langs = corrections.get("languages", {})
    for lang_id, data in parsed["languages"].items():
        found = corr_langs.get(lang_id, data["found"])
        if not found:
            continue
        weight = 2 if data["status"] == 2 else 1
        total_weight += weight
        required = data.get("cefr_required")
        profile_level = profile.get("languages", {}).get(lang_id)
        if required and profile_level:
            if CEFR_ORDER.get(profile_level, 0) >= CEFR_ORDER.get(required, 99):
                matched_weight += weight
        elif profile_level:
            # Offer mentions the language with no explicit level: just having it is enough
            matched_weight += weight

    corr_soft = corrections.get("soft_skills", {})
    for soft_id, data in parsed.get("soft_skills", {}).items():
        found = corr_soft.get(soft_id, data["found"])
        if not found:
            continue
        total_weight += 1
        if profile.get("soft_skills", {}).get(soft_id):
            matched_weight += 1

    if total_weight == 0:
        return None
    return round(100 * matched_weight / total_weight)


def run(capture_path, dossier_path, profile_path, reparse):
    skills_catalog = parse.load_skills()
    lang_catalog = parse.load_languages()
    cities_catalog = parse.load_cities()
    soft_catalog = parse.load_soft_skills()

    captured = load_json(capture_path, [])
    dossier = load_json(dossier_path, [])
    profile = load_json(profile_path, {"skills": {}, "languages": {}, "soft_skills": {}})

    dossier_by_id = {e["job_id"]: e for e in dossier}

    new_count = 0
    reparsed_count = 0
    for c in captured:
        job_id = c["job_id"]
        existing = dossier_by_id.get(job_id)

        if existing is None:
            parsed = parse.parse_offer(
                c["raw_text"], skills_catalog, lang_catalog, cities_catalog, soft_catalog
            )
            entry = {
                "job_id": job_id,
                "date_captured": c.get("date_captured"),
                "company_raw": c.get("company_raw"),
                "source": c.get("source"),
                "raw_text": c.get("raw_text"),
                "parsed": parsed,
                "corrections": {"skills": {}, "languages": {}, "soft_skills": {}, "manual_skills": []},
                "application_status": "Not applied",
                "notes": "",
                "match_percent": None,
            }
            dossier_by_id[job_id] = entry
            new_count += 1
        elif reparse:
            existing["parsed"] = parse.parse_offer(
                existing["raw_text"], skills_catalog, lang_catalog, cities_catalog, soft_catalog
            )
            reparsed_count += 1

    # Recompute match for ALL entries (cheap, and it means an updated profile
    # in review.html is reflected even if you didn't capture anything new)
    for entry in dossier_by_id.values():
        entry["match_percent"] = compute_match(entry, profile)

    final_dossier = list(dossier_by_id.values())
    save_json(dossier_path, final_dossier)

    print(f"Offers in capture file: {len(captured)}")
    print(f"Newly analyzed: {new_count}")
    if reparse:
        print(f"Re-analyzed (--reparse): {reparsed_count}")
    print(f"Total in dossier: {len(final_dossier)}")
    print(f"Saved to: {dossier_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Merges capture + parsing into the final dossier.")
    ap.add_argument("capture_file", help="JSON exported from job_capture.html")
    ap.add_argument("--dossier", default=DEFAULT_DOSSIER, help="Dossier file (created if missing)")
    ap.add_argument("--profile", default=DEFAULT_PROFILE, help="profile.json file")
    ap.add_argument("--reparse", action="store_true", help="Re-analyze existing offers (use after editing catalogs)")
    args = ap.parse_args()

    run(args.capture_file, args.dossier, args.profile, args.reparse)
