"""
coverage.py — Aggregates parse.py's results across a set of offers
and produces a report: which field is well detected, which one has gaps.
"""
import glob
import parse


def build_coverage(parsed_results):
    n = len(parsed_results)
    report = {}

    for field in ["company", "city", "canton", "workload", "workmode"]:
        found = sum(1 for r in parsed_results if r[field]["found"])
        report[field] = f"{found}/{n} ({round(100*found/n)}%)"

    skill_ids = parsed_results[0]["skills"].keys() if parsed_results else []
    skills_mentioned = sum(
        1 for r in parsed_results if any(v["found"] for v in r["skills"].values())
    )
    report["at_least_one_skill_detected"] = f"{skills_mentioned}/{n} ({round(100*skills_mentioned/n)}%)"

    langs_mentioned = sum(
        1 for r in parsed_results if any(v["found"] for v in r["languages"].values())
    )
    report["at_least_one_language_detected"] = f"{langs_mentioned}/{n} ({round(100*langs_mentioned/n)}%)"

    if parsed_results and "soft_skills" in parsed_results[0]:
        soft_mentioned = sum(
            1 for r in parsed_results if any(v["found"] for v in r["soft_skills"].values())
        )
        report["at_least_one_soft_skill_detected"] = f"{soft_mentioned}/{n} ({round(100*soft_mentioned/n)}%)"

    return report


if __name__ == "__main__":
    skills_catalog = parse.load_skills()
    lang_catalog = parse.load_languages()
    cities_catalog = parse.load_cities()
    soft_catalog = parse.load_soft_skills()

    files = sorted(glob.glob("data/raw/*.txt"))
    results = []
    for f in files:
        text = open(f, encoding="utf-8").read()
        results.append(parse.parse_offer(text, skills_catalog, lang_catalog, cities_catalog, soft_catalog))

    report = build_coverage(results)
    print(f"Coverage report — {len(files)} offers parsed\n")
    for field, value in report.items():
        print(f"  {field:35s} {value}")
