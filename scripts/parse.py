"""
parse.py — Turns raw offer text into structured fields.

Core principle: every extracted field is a dict {value, found, source}.
'found' explicitly distinguishes "not mentioned" from "mentioned but no clear value" —
never a silent empty value.
"""
import csv
import re
import unicodedata
from pathlib import Path

CATALOG_DIR = Path(__file__).parent / "catalogs"

REQUIRED_RX = re.compile(
    r"(required|requis|exig[ée]|mandatory|must\s|essential|indispensable|ma[îi]tris|"
    r"solide|proficien|fluent|courant|excellent|strong|advanced|avanc[ée]e?|imp[ée]ccable|"
    r"erforderlich|zwingend|fundiert|sehr\sgut|obbligatorio|richiest[ao]|ottima\sconoscenza|indispensabile)",
    re.I,
)
NICE_RX = re.compile(
    r"(nice\sto\shave|would\sbe\s(a\s)?(plus|asset)|is\sa\splus|atout|asset|id[ée]al|ideally|"
    r"souhait|appr[ée]ci|welcome|bonus|von\svorteil|wünschenswert|idealerweise|un\svantaggio|"
    r"preferibilmente|gradit[ao])",
    re.I,
)


def strip_accents(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn"
    ).lower().strip()


def load_aliases():
    """Returns {skill_id: [alias1, alias2, ...]} — raw alias strings, not yet compiled."""
    aliases_path = CATALOG_DIR / "aliases.csv"
    if not aliases_path.exists():
        return {}
    out = {}
    with open(aliases_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.setdefault(r["canonical_skill_id"], []).append(r["alias"])
    return out


def _pattern_with_aliases(base_pattern, skill_id, alias_map):
    """Combines the base pattern with the known aliases for this skill_id.
    An alias like 'PBI', which the main pattern (\\bPower\\s?BI\\b) wouldn't catch,
    will still be detected once added here."""
    aliases = alias_map.get(skill_id, [])
    if not aliases:
        return base_pattern
    alias_alternatives = "|".join(re.escape(a) for a in aliases)
    return f"(?:{base_pattern}|\\b(?:{alias_alternatives})\\b)"


def load_skills():
    alias_map = load_aliases()
    rows = []
    with open(CATALOG_DIR / "skills.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            pattern = _pattern_with_aliases(r["pattern"], r["skill_id"], alias_map)
            rows.append((r["skill_id"], r["canonical_name"], re.compile(pattern, re.I)))
    return rows


def load_languages():
    rows = []
    with open(CATALOG_DIR / "languages.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append((r["lang_id"], r["canonical_name"], re.compile(r["pattern"], re.I)))
    return rows


def load_soft_skills():
    path = CATALOG_DIR / "soft_skills.csv"
    if not path.exists():
        return []
    rows = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append((r["soft_id"], r["canonical_name"], re.compile(r["pattern"], re.I)))
    return rows


def load_cities():
    rows = []
    with open(CATALOG_DIR / "cities.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append((r["city"], r["canton"]))
    return rows


def detect_level(text, rx):
    """Returns (status:0/1/2, matched_window) — 0 if not found at all.
    The context window never crosses the current line, to avoid a word from
    a neighboring bullet ('Advanced Excel skills' right above) contaminating
    the detection of another bullet ('French... would be an asset')."""
    m = rx.search(text)
    if not m:
        return 0, None
    line_start = text.rfind("\n", 0, m.start()) + 1
    line_end = text.find("\n", m.end())
    if line_end == -1:
        line_end = len(text)
    # A bit of margin beyond the line, but never crossing a line break
    start = max(line_start, m.start() - 70)
    end = min(line_end, m.end() + 90)
    window = text[start:end]
    if REQUIRED_RX.search(window):
        return 2, window
    if NICE_RX.search(window):
        return 1, window
    return 1, window


CEFR_RX = re.compile(r"\b(A1|A2|B1|B2|C1|C2)\b")
NATIVE_RX = re.compile(
    r"(native|bilingu|langue\smaternelle|Muttersprache|madrelingua|mother\stongue)",
    re.I,
)


def detect_lang_cefr(window):
    """Looks for a CEFR level (A1..C2) or a 'native/bilingual' mention in the same
    text window already used for this language's required/nice-to-have status.
    Returns None if no explicit level is mentioned (the offer just says 'French' with no detail)."""
    if not window:
        return None
    m = CEFR_RX.search(window)
    if m:
        return m.group(1).upper()
    if NATIVE_RX.search(window):
        return "Native"
    return None


def detect_presence(text, rx):
    """Simple version for soft skills: no required/nice distinction,
    just 'mentioned or not', with a short excerpt as justification."""
    m = rx.search(text)
    if not m:
        return False, None
    start = max(0, m.start() - 50)
    end = min(len(text), m.end() + 60)
    return True, text[start:end].replace("\n", " ")


ACCENT_FLEX = {
    "ü": "[üu]", "é": "[ée]", "è": "[èe]", "â": "[âa]",
    "à": "[àa]", "ô": "[ôo]", "ç": "[çc]", "î": "[îi]",
}


def flexible_city_pattern(city):
    escaped = re.escape(city).replace(r"\.", r"\.?")
    for accented, cls in ACCENT_FLEX.items():
        escaped = escaped.replace(re.escape(accented), cls)
    return re.compile(r"\b" + escaped + r"\b", re.I)


def detect_city(text, cities):
    best = None  # (position, city, canton)
    for city, canton in cities:
        pattern = flexible_city_pattern(city)
        m = pattern.search(text)
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), city, canton)
    if best:
        return best[1], best[2]
    return None, None


def detect_workload(text):
    m = re.search(r"\b(\d{2,3})\s*[-–]\s*(\d{2,3})\s*%", text)
    if m:
        return f"{m.group(1)}-{m.group(2)}%", m.group(0)
    m = re.search(r"\b(\d{2,3})\s*%", text)
    if m:
        return f"{m.group(1)}%", m.group(0)
    return None, None


def detect_workmode(text):
    hybrid = re.search(r"\b(hybrid|hybride)\b", text, re.I)
    if hybrid:
        return "Hybrid", hybrid.group(0)
    remote = re.search(r"\b(remote|t[ée]l[ée]travail|travail\s[àa]\sdomicile|home\s?office|homeoffice)\b", text, re.I)
    onsite = re.search(r"\b(on-?site|sur\ssite|pr[ée]sentiel)\b", text, re.I)
    if remote and onsite:
        return "Hybrid", remote.group(0) + " / " + onsite.group(0)
    if remote:
        return "Remote", remote.group(0)
    if onsite:
        return "On-site", onsite.group(0)
    return None, None


JOB_WORDS_RX = re.compile(
    r"\b(we|nous|wir|noi|recherch|recrute|looking|suchen|cerchiamo|job|poste|position|"
    r"stelle|offre|angebot|offerta|internship|stage|company\slogo)\b",
    re.I,
)


def guess_company(text):
    head = text[:600]
    m = re.search(r"(?:Company|Employer|Entreprise|Arbeitgeber|Azienda)\s*:\s*([^\n,.;]{2,60})", head, re.I)
    if m:
        return m.group(1).strip(), m.group(0)
    m = re.search(r"\b(?:at|bei|chez|presso)\s+([A-ZÀ-ÖØ-Ý][\w&\-']*(?:\s+[A-ZÀ-ÖØ-Ý][\w&\-']*){0,3})", head)
    if m:
        return m.group(1).strip(), m.group(0)
    # Fallback: short first line, starting with a capital letter, no typical ad wording
    lines = [l.strip() for l in head.split("\n") if l.strip()]
    for line in lines[:3]:
        if 1 < len(line) < 60 and re.match(r"^[A-ZÀ-ÖØ-Ý]", line) and not JOB_WORDS_RX.search(line):
            return line, line
    return None, None


def parse_offer(raw_text, skills_catalog, lang_catalog, cities_catalog, soft_catalog=None):
    result = {}

    result["company"] = {}
    value, source = guess_company(raw_text)
    result["company"]["value"] = value
    result["company"]["found"] = value is not None
    result["company"]["source"] = source

    result["city"] = {}
    result["canton"] = {}
    city, canton = detect_city(raw_text, cities_catalog)
    result["city"]["value"] = city
    result["city"]["found"] = city is not None
    result["city"]["source"] = city
    result["canton"]["value"] = canton
    result["canton"]["found"] = canton is not None
    result["canton"]["source"] = "derived from city"

    result["workload"] = {}
    wl_value, wl_source = detect_workload(raw_text)
    result["workload"]["value"] = wl_value
    result["workload"]["found"] = wl_value is not None
    result["workload"]["source"] = wl_source

    result["workmode"] = {}
    wm_value, wm_source = detect_workmode(raw_text)
    result["workmode"]["value"] = wm_value
    result["workmode"]["found"] = wm_value is not None
    result["workmode"]["source"] = wm_source

    result["skills"] = {}
    for skill_id, label, pattern in skills_catalog:
        status, window = detect_level(raw_text, pattern)
        result["skills"][skill_id] = {"label": label, "status": status, "found": status > 0, "source": window}

    result["languages"] = {}
    for lang_id, label, pattern in lang_catalog:
        status, window = detect_level(raw_text, pattern)
        cefr = detect_lang_cefr(window)
        result["languages"][lang_id] = {
            "label": label, "status": status, "found": status > 0,
            "source": window, "cefr_required": cefr,
        }

    result["soft_skills"] = {}
    for soft_id, label, pattern in (soft_catalog or []):
        found, window = detect_presence(raw_text, pattern)
        result["soft_skills"][soft_id] = {"label": label, "found": found, "source": window}

    return result


if __name__ == "__main__":
    import sys
    import json

    skills_catalog = load_skills()
    lang_catalog = load_languages()
    cities_catalog = load_cities()
    soft_catalog = load_soft_skills()

    raw_text = Path(sys.argv[1]).read_text(encoding="utf-8")
    result = parse_offer(raw_text, skills_catalog, lang_catalog, cities_catalog, soft_catalog)
    print(json.dumps(result, indent=2, ensure_ascii=False))
