# YC Startups Context

A reproducible, source-attributed dataset of publicly listed Y Combinator companies accepted into batches from **2022 through 2026**.

The repository keeps company descriptions and useful metadata in version control, with repeatable update scripts and scheduled refreshes.

## Data

- `data/companies.csv` — spreadsheet-friendly master dataset.
- `data/companies.json` — normalized company records.
- `data/batches/YYYY.csv` — per-batch-year extracts.
- `data/metadata.json` — source, retrieval timestamp, row counts, and coverage notes.
- `data/companies_enriched.csv` / `data/companies_enriched.json` — derived product categories and business-model labels.
- `data/enrichment_queue.csv` — per-company research queue and discovery links.
- `data/verified_enrichment.csv` — source-backed founder and funding facts reviewed by a researcher, with field-specific evidence URLs.

**Coverage caveat:** The upstream API covers publicly launched companies with YC company pages; it does not guarantee every company that ever participated in YC. This project records YC batch membership, not proof of a separately disclosed funding round in that same calendar year. Funding-round amounts are not inferred.

## Data sources

- YC Startup Directory: https://www.ycombinator.com/companies/
- YC OSS API project and schema: https://github.com/yc-oss/api
- All launched companies API: https://yc-oss.github.io/api/companies/all.json
- API metadata: https://yc-oss.github.io/api/meta.json

The upstream API is an unofficial, community-maintained dataset based on YC's public company directory. This repository links back to source records and does not claim ownership of company descriptions or logos.

## Enrichment and evidence policy

The enrichment layer intentionally separates **derived classifications** from **verified facts**:

- Product category and business-model labels are heuristic classifications based on YC taxonomy; they are not presented as official company claims.
- The research queue contains discovery links, not evidence.
- `data/verified_enrichment.csv` records source-backed founder and funding facts. Every row includes the YC profile and source URLs for the reported funding facts. Amounts are labeled as a round amount or total funding where the source allows that distinction.
- Revenue values are left blank unless a reliable public source provides a sufficiently specific, dated metric. A funding announcement, valuation, hiring post, or vague growth claim is not treated as revenue.
- Missing fields remain blank. Unknown founder surnames, round types, investor lists, and dates are not inferred.
- Funding amounts are stored in USD. Dates refer to the announcement date when an exact round-close date is not public; notes describe material limitations.

The verified file is an **initial researched tranche**, not a claim that all 3,102 companies have been individually researched. It will be expanded in batches and should be treated as a point-in-time record, not a live financial database.

## Refresh locally

Requires Python 3.10+; no third-party packages are required.

```bash
python scripts/build_dataset.py
python scripts/enrich_dataset.py
```

The scripts fetch the upstream API, select batches from 2022–2026, normalize records, and write CSV, JSON, yearly extracts, metadata, derived classifications, and the research queue. The manually reviewed `verified_enrichment.csv` is maintained separately so routine refreshes do not overwrite source-reviewed facts.

## Automation

GitHub Actions refreshes the base dataset and derived enrichment on a schedule, manually via **Actions → Update YC dataset → Run workflow**, and when relevant scripts change. Generated data changes are committed only when files differ.

## License and attribution

Dataset compilation and scripts are provided under the MIT License. Upstream company descriptions and other source fields remain attributable to their original sources; review YC and upstream repository terms before redistributing commercially.
