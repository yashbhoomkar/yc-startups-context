#!/usr/bin/env python3
"""Build a normalized YC startup dataset for batches 2022–2026.

Source: the community-maintained yc-oss/api public JSON endpoint.
No company descriptions, funding amounts, or statuses are invented.
"""
from __future__ import annotations

import csv
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
BASE_URL = "https://yc-oss.github.io/api"
COMPANIES_URL = f"{BASE_URL}/companies/all.json"
META_URL = f"{BASE_URL}/meta.json"
MIN_YEAR = 2022
MAX_YEAR = 2026
USER_AGENT = "yc-startups-context-dataset/1.0 (+https://github.com/yashbhoomkar/yc-startups-context)"

FIELDS = [
    "name", "batch", "batch_year", "description", "one_liner", "website",
    "yc_url", "slug", "former_names", "industry", "subindustry", "industries",
    "tags", "locations", "regions", "team_size", "status", "stage",
    "launched_at", "launched_at_utc", "is_hiring", "nonprofit",
    "top_company", "source_api", "source_directory", "source_last_updated",
]


def fetch_json(url: str) -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            if response.status != 200:
                raise RuntimeError(f"HTTP {response.status} while fetching {url}")
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not fetch valid JSON from {url}: {exc}") from exc


def batch_year(batch: Any) -> int | None:
    """Read common YC batch labels such as W22, S22, F22, SP26 or Winter 2022."""
    if not isinstance(batch, str):
        return None
    value = batch.strip()
    match = re.search(r"(?:19|20)?(\d{2})\s*$", value)
    if not match:
        return None
    short_year = int(match.group(1))
    # YC batch labels use two-digit years; avoid treating unrelated strings as years.
    year = 2000 + short_year if short_year <= 79 else 1900 + short_year
    if not re.search(r"(?i)(winter|summer|spring|fall|autumn|^(?:W|S|F|SP|SU|WI|FA)\s*\d)", value):
        return None
    return year


def clean_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if item is not None and str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [part.strip() for part in value.split(";") if part.strip()]
    return []


def normalize(company: dict[str, Any], source_updated: str | None) -> dict[str, Any]:
    batch = company.get("batch")
    year = batch_year(batch)
    launched_at = company.get("launched_at")
    launched_at_utc = None
    if isinstance(launched_at, (int, float)) and launched_at > 0:
        launched_at_utc = datetime.fromtimestamp(launched_at, tz=timezone.utc).isoformat()
    locations = company.get("all_locations", company.get("locations", []))
    if isinstance(locations, str):
        locations = [part.strip() for part in locations.split(";") if part.strip()]
        if not locations and company.get("all_locations"):
            locations = [company["all_locations"].strip()]
    record = {
        "name": company.get("name") or "",
        "batch": batch or "",
        "batch_year": year,
        "description": company.get("long_description") or "",
        "one_liner": company.get("one_liner") or "",
        "website": company.get("website") or "",
        "yc_url": company.get("url") or "",
        "slug": company.get("slug") or "",
        "former_names": clean_list(company.get("former_names")),
        "industry": company.get("industry") or "",
        "subindustry": company.get("subindustry") or "",
        "industries": clean_list(company.get("industries")),
        "tags": clean_list(company.get("tags")),
        "locations": locations if isinstance(locations, list) else [],
        "regions": clean_list(company.get("regions")),
        "team_size": company.get("team_size"),
        "status": company.get("status") or "",
        "stage": company.get("stage") or "",
        "launched_at": launched_at,
        "launched_at_utc": launched_at_utc,
        "is_hiring": company.get("isHiring"),
        "nonprofit": company.get("nonprofit"),
        "top_company": company.get("top_company"),
        "source_api": company.get("api") or COMPANIES_URL,
        "source_directory": company.get("url") or "https://www.ycombinator.com/companies/",
        "source_last_updated": source_updated,
    }
    return record


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            row = dict(record)
            for key in ("former_names", "industries", "tags", "locations", "regions"):
                row[key] = " | ".join(row.get(key) or [])
            writer.writerow(row)


def main() -> int:
    print(f"Fetching {META_URL}", flush=True)
    meta = fetch_json(META_URL)
    source_updated = meta.get("last_updated") if isinstance(meta, dict) else None

    print(f"Fetching {COMPANIES_URL}", flush=True)
    companies = fetch_json(COMPANIES_URL)
    if not isinstance(companies, list):
        raise RuntimeError("Unexpected upstream schema: companies endpoint must return an array")

    records = []
    seen = set()
    excluded_no_batch = 0
    for company in companies:
        if not isinstance(company, dict):
            continue
        record = normalize(company, source_updated)
        year = record["batch_year"]
        if year is None:
            excluded_no_batch += 1
            continue
        if MIN_YEAR <= year <= MAX_YEAR:
            key = (str(company.get("id") or ""), record["name"].casefold(), record["batch"])
            if key in seen:
                continue
            seen.add(key)
            records.append(record)

    records.sort(key=lambda r: (r["batch_year"] or 0, r["batch"], r["name"].casefold()))
    if not records:
        raise RuntimeError("No matching records found; refusing to overwrite dataset with an empty result")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    write_json(DATA_DIR / "companies.json", records)
    write_csv(DATA_DIR / "companies.csv", records)

    batch_dir = DATA_DIR / "batches"
    for year in range(MIN_YEAR, MAX_YEAR + 1):
        year_records = [r for r in records if r["batch_year"] == year]
        write_csv(batch_dir / f"{year}.csv", year_records)

    batch_counts: dict[str, int] = {}
    for record in records:
        batch_counts[record["batch"]] = batch_counts.get(record["batch"], 0) + 1

    metadata = {
        "dataset": "YC Startups Context",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_last_updated": source_updated,
        "source_metadata_url": META_URL,
        "source_companies_url": COMPANIES_URL,
        "scope": {"batch_year_min": MIN_YEAR, "batch_year_max": MAX_YEAR},
        "source_total_companies": len(companies),
        "included_companies": len(records),
        "excluded_records_without_recognized_batch": excluded_no_batch,
        "counts_by_batch": dict(sorted(batch_counts.items())),
        "coverage_note": "Upstream data includes publicly launched companies with YC directory pages; it may omit companies without public launch pages. Batch year indicates YC cohort, not necessarily an external funding-round year.",
        "fields": FIELDS,
    }
    write_json(DATA_DIR / "metadata.json", metadata)
    print(f"Wrote {len(records)} companies to {DATA_DIR}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
