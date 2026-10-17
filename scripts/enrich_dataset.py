#!/usr/bin/env python3
"""Create an evidence-first enrichment layer over the YC directory dataset.

YC's public directory does not reliably publish founders, funding rounds, investors,
or revenue for every company. Those fields remain empty until a researcher supplies
a source URL and evidence. This script derives only transparent categories from
published YC tags/industry fields and generates research links; it does not invent
financial facts.
"""
from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
INPUT = DATA_DIR / "companies.json"
OUTPUT_JSON = DATA_DIR / "companies_enriched.json"
OUTPUT_CSV = DATA_DIR / "companies_enriched.csv"
QUEUE_CSV = DATA_DIR / "enrichment_queue.csv"
META = DATA_DIR / "enrichment_metadata.json"
VERIFIED = DATA_DIR / "verified_enrichment.csv"

ADDITIONAL_FIELDS = [
    "product_category_derived",
    "business_model_derived",
    "category_derivation_basis",
    "founders_public",
    "funding_total_usd",
    "funding_last_round",
    "funding_last_round_amount_usd",
    "funding_last_round_date",
    "investors",
    "investors_source_url",
    "revenue_estimate_usd",
    "revenue_estimate_as_of",
    "founders_source_url",
    "funding_source_url",
    "revenue_source_url",
    "enrichment_status",
    "enrichment_notes",
    "founder_research_url",
    "funding_research_url",
    "revenue_research_url",
    "investor_research_url",
]

def as_text(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return " | ".join(str(x) for x in value if x is not None and str(x).strip())
    return str(value)

def product_category(company):
    """Transparent rule-based label based on YC's own taxonomy; not a verified claim."""
    parts = [company.get("industry", ""), company.get("subindustry", "")]
    tags = company.get("tags") or []
    parts.extend(tags if isinstance(tags, list) else [tags])
    text = " ".join(str(x) for x in parts).lower()
    rules = [
        (r"developer tools|devtool|software development|code review|coding|api|infrastructure|database|observability|devops|cloud", "Developer infrastructure & tools"),
        (r"artificial intelligence|\bai\b|machine learning|generative ai|llm|ai assistant", "AI / machine learning"),
        (r"fintech|payments|banking|lending|insurance|financial|accounting|wealth", "Financial technology"),
        (r"healthcare|health tech|medical|diagnostic|therapeutic|biotech|drug discovery", "Healthcare & life sciences"),
        (r"robotics|manufacturing|hardware|industrial|aerospace|drones|defense", "Industrial & hard tech"),
        (r"climate|energy|sustainab|carbon|agriculture", "Climate, energy & agriculture"),
        (r"marketplace|e-commerce|retail|consumer goods", "Commerce & marketplaces"),
        (r"education|edtech|learning", "Education & learning"),
        (r"security|cybersecurity|compliance|identity", "Security & compliance"),
        (r"real estate|construction|property", "Real estate & construction"),
        (r"logistics|supply chain|transportation|shipping", "Logistics & mobility"),
    ]
    for pattern, label in rules:
        if re.search(pattern, text):
            return label, "YC industry/subindustry/tags (rule-based)"
    industry = company.get("industry") or ""
    if industry:
        return str(industry), "YC industry (fallback)"
    return "Unclassified", "No usable YC taxonomy fields"

def business_model(company):
    parts = [company.get("industry", ""), company.get("subindustry", "")]
    tags = company.get("tags") or []
    parts.extend(tags if isinstance(tags, list) else [tags])
    text = " ".join(str(x) for x in parts).lower()
    labels = []
    if re.search(r"marketplace|two-sided|buyers and sellers", text):
        labels.append("Marketplace")
    if re.search(r"saas|b2b|enterprise|business software|productivity|developer tools|api", text):
        labels.append("B2B software / SaaS (taxonomy-derived)")
    if re.search(r"consumer|social|gaming|e-commerce|direct-to-consumer", text):
        labels.append("Consumer-facing (taxonomy-derived)")
    if re.search(r"fintech|payments|lending|insurance|banking", text):
        labels.append("Financial services (taxonomy-derived)")
    if re.search(r"hardware|robotics|manufacturing|industrial", text):
        labels.append("Hardware / physical products (taxonomy-derived)")
    return " | ".join(dict.fromkeys(labels)) if labels else "Unknown"

def query_url(company, topic):
    name = company.get("name", "")
    website = company.get("website", "")
    query = {
        "founders": f'"{name}" founders founder CEO',
        "funding": f'"{name}" startup funding raised investors round',
        "revenue": f'"{name}" revenue ARR annual recurring revenue',
        "investors": f'"{name}" investors funding venture capital',
    }[topic]
    if website:
        query += f' "{website}"'
    return "https://www.google.com/search?q=" + quote_plus(query)

def main():
    if not INPUT.exists():
        raise SystemExit(f"Missing {INPUT}; run scripts/build_dataset.py first")
    companies = json.loads(INPUT.read_text(encoding="utf-8"))
    if not isinstance(companies, list) or not companies:
        raise SystemExit("Input dataset is empty or invalid; refusing to overwrite enrichment outputs")

    verified_by_name = {}
    if VERIFIED.exists():
        with VERIFIED.open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                key = (row.get("company") or "").strip().casefold()
                if key:
                    if key in verified_by_name:
                        raise SystemExit(f"Duplicate company in {VERIFIED}: {row.get('company')}")
                    if row.get("verification_status") != "verified":
                        raise SystemExit(f"Unverified record in {VERIFIED}: {row.get('company')}")
                    if not row.get("yc_profile_url") or not row.get("founders_source_url") or not row.get("funding_source_url"):
                        raise SystemExit(f"Missing required evidence URL in {VERIFIED}: {row.get('company')}")
                    verified_by_name[key] = row

    enriched = []
    queue = []
    for source in companies:
        company = dict(source)
        category, basis = product_category(company)
        model = business_model(company)
        company.update({
            "product_category_derived": category,
            "business_model_derived": model,
            "category_derivation_basis": basis,
            # Unknown facts intentionally remain empty until evidence is reviewed.
            "founders_public": "",
            "funding_total_usd": "",
            "funding_last_round": "",
            "funding_last_round_amount_usd": "",
            "funding_last_round_date": "",
            "investors": "",
            "investors_source_url": "",
            "revenue_estimate_usd": "",
            "revenue_estimate_as_of": "",
            "founders_source_url": "",
            "funding_source_url": "",
            "revenue_source_url": "",
            "enrichment_status": "pending_source_verification",
            "enrichment_notes": "Financial/founder facts not populated without a verifiable public source.",
            "founder_research_url": query_url(source, "founders"),
            "funding_research_url": query_url(source, "funding"),
            "revenue_research_url": query_url(source, "revenue"),
            "investor_research_url": query_url(source, "investors"),
        })
        evidence = verified_by_name.get((company.get("name") or "").strip().casefold())
        if evidence:
            company["founders_public"] = evidence.get("founders_public", "")
            round_label = evidence.get("funding_last_round", "")
            amount = evidence.get("funding_amount_usd", "")
            if round_label.startswith("Disclosed total funding"):
                company["funding_total_usd"] = amount
                company["funding_last_round"] = ""
                company["funding_last_round_amount_usd"] = ""
            else:
                company["funding_last_round"] = round_label
                company["funding_last_round_amount_usd"] = amount
            company["funding_last_round_date"] = evidence.get("funding_date", "")
            company["investors"] = evidence.get("investors", "")
            company["founders_source_url"] = evidence.get("founders_source_url", "")
            company["funding_source_url"] = evidence.get("funding_source_url", "")
            company["investors_source_url"] = evidence.get("investors_source_url", "")
            company["enrichment_status"] = "verified_partial"
            company["enrichment_notes"] = evidence.get("notes", "")
        enriched.append(company)
        queue.append({
            "name": company.get("name", ""),
            "batch": company.get("batch", ""),
            "batch_year": company.get("batch_year", ""),
            "yc_url": company.get("yc_url", ""),
            "website": company.get("website", ""),
            "product_category_derived": category,
            "business_model_derived": model,
            "founders_public": company.get("founders_public", ""),
            "founders_source_url": company.get("founders_source_url", ""),
            "funding_total_usd": company.get("funding_total_usd", ""),
            "funding_last_round": company.get("funding_last_round", ""),
            "funding_last_round_amount_usd": company.get("funding_last_round_amount_usd", ""),
            "funding_last_round_date": company.get("funding_last_round_date", ""),
            "funding_source_url": company.get("funding_source_url", ""),
            "investors": company.get("investors", ""),
            "investor_source_url": company.get("investors_source_url", ""),
            "revenue_estimate_usd": "",
            "revenue_estimate_as_of": "",
            "revenue_source_url": "",
            "research_status": company.get("enrichment_status", "pending_source_verification"),
            "notes": company.get("enrichment_notes", ""),
            "founder_research_url": query_url(source, "founders"),
            "funding_research_url": query_url(source, "funding"),
            "investor_research_url": query_url(source, "investors"),
            "revenue_research_url": query_url(source, "revenue"),
        })

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(enriched, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    def write_csv(path, rows):
        fields = list(rows[0].keys())
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow({k: as_text(v) for k, v in row.items()})
    write_csv(OUTPUT_CSV, enriched)
    write_csv(QUEUE_CSV, queue)

    category_counts = {}
    for row in enriched:
        category_counts[row["product_category_derived"]] = category_counts.get(row["product_category_derived"], 0) + 1
    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input": "data/companies.json",
        "companies_enriched": len(enriched),
        "outputs": ["data/companies_enriched.csv", "data/companies_enriched.json", "data/enrichment_queue.csv"],
        "automatically_derived_fields": ["product_category_derived", "business_model_derived"],
        "manual_evidence_fields": ["founders_public", "funding_total_usd", "funding_last_round", "funding_last_round_amount_usd", "funding_last_round_date", "investors", "revenue_estimate_usd"],
        "verified_records_loaded": len(verified_by_name),
        "verified_records_source": "data/verified_enrichment.csv",
        "evidence_policy": "Do not enter founder, funding, investor, or revenue claims without a source URL. Leave unknowns empty. Do not treat search-result snippets as verified evidence.",
        "category_counts": dict(sorted(category_counts.items())),
        "coverage_note": "Product category and business model are heuristic labels derived from YC taxonomy. Source-reviewed facts are merged from data/verified_enrichment.csv; all other founder, funding, investor and revenue fields remain blank pending source verification.",
    }
    META.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Enriched {len(enriched)} records; wrote CSV, JSON, research queue and metadata.")

if __name__ == "__main__":
    main()
