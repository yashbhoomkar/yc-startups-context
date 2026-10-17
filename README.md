# YC Startups Context

A reproducible, source-attributed dataset of publicly listed Y Combinator companies accepted into batches from **2022 through 2026**.

The repository is designed to keep company descriptions and useful metadata in version control, with a repeatable update script and scheduled refreshes.

## Data

After the first successful data refresh, generated files will be available under `data/`:

- `companies.csv` — spreadsheet-friendly master dataset.
- `companies.json` — normalized company records.
- `batches/YYYY.csv` — per-batch-year extracts.
- `metadata.json` — source, retrieval timestamp, row counts, and coverage notes.

**Coverage caveat:** The upstream API covers publicly launched companies with YC company pages; it does not guarantee every company that ever participated in YC. This project records YC batch membership, not proof of a separately disclosed funding round in that same calendar year. Funding-round amounts are not inferred.

## Data source

- YC Startup Directory: https://www.ycombinator.com/companies/
- YC OSS API project and schema: https://github.com/yc-oss/api
- All launched companies API: https://yc-oss.github.io/api/companies/all.json
- API metadata: https://yc-oss.github.io/api/meta.json

The upstream API is an unofficial, community-maintained dataset based on YC's public company directory. See its repository for provenance and schema details. This repository links back to source records and does not claim ownership of company descriptions or logos.

## Fields

The normalized records include company name, batch, description, one-liner, YC profile, company website, industries, subindustry, tags, locations, team size, status, stage, launch timestamp, and source URL where available. Missing source fields remain empty/null rather than being fabricated.

## Refresh locally

Requires Python 3.10+; no third-party packages are required.

```bash
python scripts/build_dataset.py
```

The script fetches the upstream API, selects batches from 2022–2026, normalizes records, and writes CSV, JSON, yearly extracts, and metadata into `data/`.

## Automation

GitHub Actions can refresh the dataset on a schedule or manually via **Actions → Update YC dataset → Run workflow**. Generated data changes are committed only when the files differ.

## License and attribution

Dataset compilation and scripts are provided under the MIT License. Upstream company descriptions and other source fields remain attributable to their original sources; review YC and upstream repository terms before redistributing commercially.
