# Critical Analysis of YC Startup Dataset (2022–2026)

**Prepared:** 17 October 2026  
**Repository:** [yashbhoomkar/yc-startups-context](https://github.com/yashbhoomkar/yc-startups-context)  
**Dataset snapshot:** 3,102 companies; upstream metadata last updated 17 October 2026 02:13 UTC  
**Purpose:** Assess what the current dataset can reliably tell us about startup patterns and product opportunities—and what it cannot.

## Executive conclusion

The dataset is useful as a **startup-discovery index**, not yet as a validated market-intelligence or investment dataset. It contains 3,102 publicly listed YC companies in batches from 2022 through 2026, with strong coverage of names, batch, industry taxonomy, websites, and team-size estimates. It does **not** currently contain enough source-verified funding, revenue, customer, pricing, retention, or competitive data to identify statistically which business models succeed.

The most actionable signal is structural rather than predictive: the directory is heavily B2B-oriented, the median listed team size is four, and engineering/product/design plus infrastructure are prominent B2B subcategories. That supports investigating products that solve narrow operational problems for small software businesses. It does not prove those businesses are underserved, willing to pay, or attractive customers.

**Recommendation:** Do not pick a product simply because it is a popular YC category. Use the dataset to produce a shortlist of narrowly defined customer problems, then enrich that shortlist with competitor capabilities, pricing, customer complaints, evidence of demand, and realistic distribution economics. For the stated goal—building alongside a full-time job in under five hours per week—prefer a small, self-serve B2B product with limited integrations and low ongoing support burden.

## 1. Scope and method

This analysis used the committed repository files as they existed on 17 October 2026:
- [README and dataset policy](../README.md)
- [Base dataset metadata](../data/metadata.json)
- [Derived-category metadata](../data/enrichment_metadata.json)
- [Yearly batch extracts](../data/batches/)
- [Source-reviewed enrichment](../data/verified_enrichment.csv)
- [Dataset builder](../scripts/build_dataset.py)
- [Enrichment script](../scripts/enrich_dataset.py)

The five annual CSV extracts were parsed and counted. Counts and missingness below describe the repository snapshot, not a live YC API query. Category counts come from the repository's rule-based enrichment metadata.

The upstream source is a community-maintained API derived from YC's public company directory. The repo itself explicitly notes that companies without public launch pages may be absent. The dataset's cohort year is the YC batch year; it is not necessarily a funding-round year.

## 2. Dataset composition

### Companies by YC batch year

| Batch year | Companies | Share of 3,102 |
|---|---:|---:|
| 2022 | 631 | 20.3% |
| 2023 | 494 | 15.9% |
| 2024 | 590 | 19.0% |
| 2025 | 621 | 20.0% |
| 2026 | 766 | 24.7% |
| **Total** | **3,102** | **100%** |

The larger 2026 count should not be interpreted as proof that YC is growing at that rate or that the 2026 startup market is larger. Batch structures, source coverage, public-launch timing, and the snapshot date all affect these counts. The dataset is a selected directory cohort, not a census of startups founded in each year.

### Core-field coverage

| Field | Populated | Missing | Coverage |
|---|---:|---:|---:|
| Company name | 3,102 | 0 | 100.0% |
| Batch | 3,102 | 0 | 100.0% |
| Industry / subindustry | 3,102 | 0 | 100.0% |
| One-liner | 3,088 | 14 | 99.5% |
| Website | 3,087 | 15 | 99.5% |
| Long description | 2,978 | 124 | 96.0% |
| Tags | 2,482 | 620 | 80.0% |
| Locations | 3,022 | 80 | 97.4% |
| Team size | 3,047 | 55 | 98.2% |
| YC profile URL | 3,102 | 0 | 100.0% |

This is good coverage for **discovery and segmentation**. It is not good coverage for commercial diligence. High description coverage does not mean descriptions are independent, current, comparable, or detailed enough to establish a customer's pain or a company's business model.

## 3. What the directory says about company types

### Official/base YC industry field

| YC industry | Companies | Share |
|---|---:|---:|
| B2B | 1,841 | 59.3% |
| Fintech | 319 | 10.3% |
| Industrials | 295 | 9.5% |
| Healthcare | 287 | 9.3% |
| Consumer | 233 | 7.5% |
| Real Estate and Construction | 72 | 2.3% |
| Education | 33 | 1.1% |
| Government | 22 | 0.7% |

B2B is the dominant base industry in this snapshot. This is a meaningful starting point for a founder who wants to investigate business customers, but it is not a measure of market size, revenue, growth, or customer willingness to pay.

### Rule-derived product categories

| Derived category | Companies | Share |
|---|---:|---:|
| AI / machine learning | 1,241 | 40.0% |
| Developer infrastructure & tools | 592 | 19.1% |
| B2B (residual derived label) | 388 | 12.5% |
| Financial technology | 285 | 9.2% |
| Industrial & hard tech | 191 | 6.2% |
| Healthcare & life sciences | 170 | 5.5% |
| Consumer | 58 | 1.9% |
| Commerce & marketplaces | 50 | 1.6% |
| Security & compliance | 30 | 1.0% |
| Logistics & mobility | 28 | 0.9% |
| Real estate & construction | 28 | 0.9% |
| Education & learning | 21 | 0.7% |
| Climate, energy & agriculture | 10 | 0.3% |
| Government | 10 | 0.3% |

**Critical caveat:** These derived categories are not mutually equivalent to YC's official industry taxonomy. The enrichment script applies ordered keyword rules and assigns the first match. For example, a B2B company whose tags mention AI or infrastructure may be assigned to AI or developer tools rather than the residual “B2B” category. Thus, “B2B = 388” in this table does **not** contradict the 1,841 companies in YC's base B2B industry, and it must not be reported as the total B2B market.

The high AI/ML count shows that AI-related language is common in this directory. It does not establish that AI is the best market to enter. It may indicate opportunity, competition, or both. A category count alone cannot distinguish these.

### Useful B2B subcategory clues

Some of the largest base taxonomy subcategories include:
- B2B → Engineering, Product and Design: **377**
- B2B → Infrastructure: **208**
- B2B → Productivity: **97**
- B2B → Operations: **89**
- B2B → Sales: **80**
- B2B → Finance and Accounting: **76**
- B2B → Supply Chain and Logistics: **72**
- B2B → Security: **70**
- B2B → Marketing: **64**
- B2B → Analytics: **63**

These counts are useful for organizing research, not for measuring unmet demand. The next question is not “which subcategory has many startups?” It is “which recurring workflow is expensive or painful, what do current tools fail to do, and can a new entrant reach buyers cheaply?”

## 4. Team size and operating model

For the 3,009 records with a parseable positive team-size value:
- Median team size: **4**
- 75th percentile: **8**
- 90th percentile: **20**
- 95th percentile: **35**
- Maximum: **3,600**
- More than 20 employees: **285 records**
- More than 100 employees: **20 records**

The distribution is strongly skewed: most companies are small, while a few large values pull the maximum upward. The median and percentiles are more informative than the average would be.

**Implication:** Small-team workflows may be worth investigating because a small product can sometimes solve a concrete problem without a large enterprise sales motion. However, YC directory team size is a noisy, time-sensitive proxy. It does not tell us whether a company is bootstrapped, has a large budget, or will buy from an unknown vendor.

A useful follow-up analysis should segment small teams by product category and look for operational dependencies: external APIs, CI/CD, database migrations, customer onboarding, compliance evidence, support operations, and data synchronization. Each is a hypothesis to test, not a proven gap.

## 5. Status, hiring, and cohort-age bias

### Current directory status

| Status | Companies | Share |
|---|---:|---:|
| Active | 2,754 | 88.8% |
| Inactive | 202 | 6.5% |
| Acquired | 146 | 4.7% |
| **Total** | **3,102** | **100%** |

The directory marks 976 companies as hiring (31.5%) and 2,126 as not hiring (68.5%).

These values should be treated as **directory status indicators**, not audited operating outcomes. “Active” does not mean profitable, growing, or even generating meaningful revenue. “Inactive” may be delayed or inconsistently updated. “Acquired” is an outcome label, not a measure of acquisition price or investor return. Hiring flags can become stale.

Older cohorts have had more time to be marked inactive or acquired. For that reason, comparing status percentages by batch year is not a clean survival analysis. The apparent higher active share among newer batches is expected to be affected by this unequal observation window.

To measure survival more credibly, we would need timestamped status histories or independently verified shutdown/acquisition dates, a defined observation window, and careful treatment of right-censoring. The current snapshot cannot provide that.

## 6. Geography and India relevance

The region field identifies **64 records** with “India | South Asia” in the region string, about **2.1%** of the dataset. This is a directory-location classification, not a founder-nationality field; it also does not capture every Indian founder or India-focused business. Some companies are remote and have multiple region labels.

Among those 64 records, the base industries include 34 B2B, 16 fintech, 5 consumer, 4 education, 3 healthcare, and 2 real estate/construction companies. This is a small and selection-biased subset, not a representative sample of India's startup market.

For a founder based in India, the practical opportunity may be either:
1. sell globally to software teams using self-serve acquisition, or
2. solve a locally specific workflow with demonstrable willingness to pay.

The dataset alone cannot decide between these. Local purchasing power, compliance, integrations, support expectations, and customer acquisition channels need separate validation.

## 7. The largest analytical weakness: missing business evidence

The enrichment layer contains **9 source-verified records out of 3,102**—approximately **0.29%**. The repository's evidence policy is appropriately conservative, but the dataset is not yet enriched enough for comparative business analysis.

Current evidence gaps include:

- **Revenue / ARR:** no reliable, systematic revenue field coverage.
- **Pricing:** no structured pricing data.
- **Customer profile:** no normalized ICP, buyer, use case, or customer segment.
- **Traction:** no comparable customer counts, usage, retention, or growth series.
- **Funding:** only a small, manually verified tranche; funding facts are not comprehensive.
- **Competitors:** no structured competitor set or feature/pricing comparison.
- **Outcome history:** no event timeline for shutdowns, acquisitions, pivots, or status changes.
- **Founder attributes:** only a few source-verified records.
- **Evidence freshness:** no systematic field-level refresh schedule for commercial facts.

This creates a severe selection problem: if we look only at famous companies with public funding news, we will over-sample visible winners and miss quiet, profitable, bootstrapped companies. Funding announcements also reflect investor incentives and market conditions, not necessarily durable customer demand.

**Do not infer revenue from funding, valuation, hiring, or an enthusiastic launch post.** Do not treat an absent value as zero. The current scripts correctly leave unknown financial facts blank; preserve that behavior.

## 8. Data-engineering and taxonomy risks

### Strengths
- Reproducible Python scripts produce normalized CSV and JSON outputs.
- The source URL and retrieval metadata are retained.
- The enrichment script separates heuristic categories from source-verified facts.
- Unknown funding and founder facts are left blank instead of being guessed.
- GitHub Actions refreshes the dataset weekly and can be triggered manually.
- The verified enrichment file is kept separate from automatically regenerated data.

### Weaknesses and risks to address
1. **No durable source ID in normalized output.** The builder uses the upstream ID in its deduplication key but does not include that ID in the final field list. Persist a stable upstream ID so records can be reconciled across refreshes even when names, slugs, or websites change.
2. **Company-name-only enrichment matching.** Verified enrichment is joined to the master data by case-folded company name. Names are not guaranteed unique: the snapshot contains 29 name keys appearing more than once. Even when repeated names represent different companies, name-only matching can attach evidence to the wrong record. Match on stable ID and/or YC profile URL, with explicit collision handling.
3. **Single-label, ordered keyword taxonomy.** The first matching keyword rule wins. Categories can hide cross-cutting attributes (for example, a B2B infrastructure product with an AI component). Keep the original YC taxonomy and use multi-label derived tags or confidence scores for analysis.
4. **Limited validation of upstream schema and semantics.** The builder validates that the endpoint returns an array and that the result is non-empty, but production-quality analytics should also validate expected fields, ID uniqueness, date ranges, batch distribution shifts, and anomalous changes before committing refreshed data.
5. **Current status and team size are snapshots.** Their source timestamps and historical values are not maintained as time series. Trends over time cannot be inferred from repeated snapshots unless snapshots are preserved.
6. **Category derivation is not a market taxonomy.** Rule changes can alter historical category counts. Version the taxonomy and record the derivation version.
7. **“Top company” currently has no positive values in this snapshot.** That field is not useful for ranking this extract unless its source meaning and refresh behavior are clarified.

These are data-quality limitations, not evidence that the repository is unusable. The current design is a solid foundation for discovery; the next step is to make identity, provenance, and longitudinal analysis more reliable.

## 9. Product opportunity implications

The dataset supports several **research directions**, but not a defensible final product choice yet.

### Hypothesis A: A narrowly scoped integration reliability product
Target a specific type of small SaaS company that depends on one or two external APIs. Investigate recurring failures such as API version changes, broken examples, schema drift, and hard-to-reproduce integration errors.

Why it is worth investigating: B2B and infrastructure companies are numerous, and small teams may lack dedicated integration reliability staff.

Why it may fail: API monitoring, contract testing, and documentation testing are established categories. A generic “AI fixes your integrations” pitch is not differentiation. Select one ecosystem and demonstrate a measurable reduction in incident/debugging time.

### Hypothesis B: A migration safety tool for a narrow stack
Investigate whether teams using a specific database/framework combination struggle to rehearse schema migrations, identify lock risk, or understand rollback safety.

Why it is worth investigating: the workflow is consequential and can be tied to engineering risk.

Why it may fail: production data handling, correctness expectations, and trust are high barriers. A broad database platform would exceed a five-hour-per-week maintenance budget.

### Hypothesis C: A codebase onboarding / archaeology product
Investigate whether small engineering teams need a repeatable way to help new developers understand a real repository, trace requests, and safely complete their first change.

Why it is worth investigating: engineering/product/design is a prominent YC subcategory, and the product could start with guided workflows rather than expensive AI inference.

Why it may fail: willingness to pay and recurring usage are uncertain; this could become a content business rather than a software company.

### Hypothesis D: A non-developer vertical workflow
Select a narrow workflow in operations, supply chain, accounting, or customer onboarding. Find a repetitive process where a small business currently uses spreadsheets, email, and manual checks.

Why it is worth investigating: the B2B taxonomy spans many operational functions beyond developer tools.

Why it may fail: the current dataset gives us labels, not workflow-level customer evidence. Some verticals require domain knowledge and sales effort that may conflict with the user's time constraints.

### Preliminary ranking for further research

| Hypothesis | Fit with low time / self-serve | Key unknown | Decision |
|---|---|---|---|
| Narrow integration reliability | Medium–high if scope is one ecosystem | Competitive gap and willingness to pay | Research first |
| Narrow migration safety | Medium | Trust, support load, technical risk | Research second |
| Codebase onboarding lab | High for content delivery; uncertain recurring revenue | Repeat use and budget owner | Validate cheaply |
| Vertical operations workflow | Potentially high recurring value | Domain expertise and distribution | Explore after choosing a specific workflow |

These are research priorities, not a declaration that one is already a viable business. The YC data is a starting map, not the evidence that closes the decision.

## 10. Recommended next analysis pipeline

### Phase 1 — Improve data reliability
1. Persist stable upstream company IDs.
2. Join verified facts by stable ID or YC profile URL, not company name alone.
3. Add automated checks for duplicate IDs, missing URLs, invalid dates, category shifts, and unexpected batch-count changes.
4. Preserve dated snapshots to build a longitudinal status history.
5. Add taxonomy versioning and multi-label tags.

### Phase 2 — Build a research-ready company table
For a prioritized subset of 100–200 companies, capture only source-backed fields:
- specific product / workflow;
- ideal customer profile and economic buyer;
- pricing and billing unit;
- customer evidence and dated traction claims;
- named competitors and their feature/pricing pages;
- public complaints or unmet needs, with original URLs;
- funding round, total funding, and date as separate concepts;
- source URL, date checked, evidence type, and confidence.

Do not enrich all 3,102 records equally at first. Prioritize categories relevant to the product hypotheses, then sample less-visible companies to reduce winner/survivorship bias.

### Phase 3 — Search for customer pain, not startup popularity
For each shortlisted workflow:
1. Read competitor documentation and pricing pages.
2. Find repeated complaints from actual users and distinguish anecdotes from patterns.
3. Identify a narrowly defined customer with a costly, frequent problem.
4. Test a landing page or a small demo before building a full platform.
5. Ask for a concrete commitment—paid pilot, preorder where appropriate, or permission to run a real workflow—not just positive feedback.
6. Estimate acquisition cost, support burden, and gross margin.
7. Reject the idea if distribution requires repeated high-touch sales or if ongoing support exceeds the available time.

### Phase 4 — Apply a decision scorecard
Score each opportunity from 1–5 on:
- pain severity and frequency;
- evidence customers already spend money or time on it;
- weakness of existing solutions;
- clear differentiation for a small entrant;
- self-serve distribution potential;
- time to a paid test;
- recurring-revenue potential;
- maintenance and support burden;
- infrastructure / AI cost;
- compliance compatibility with the user's employment.

Require source links for every score that depends on an external fact. Keep subjective founder-fit judgments separate from measured evidence. Do not turn the score into a false-precision “market opportunity” number.

## Final verdict

The current dataset is **good enough to discover and organize startup ideas, but not good enough to tell us which idea will make money**. It shows that B2B and developer-facing companies are common in the YC directory and that many listed teams are small. It does not establish unmet demand, competitor weakness, revenue potential, or customer acquisition feasibility.

The next high-value asset is not a larger unfiltered startup list. It is a **small, deeply researched evidence table** connecting a real workflow problem to customers, competing products, pricing, and proof of willingness to pay. Start with 100–200 relevant companies, verify claims at the source, and use that evidence to decide whether to build.

### Source links
- [Repository README](https://github.com/yashbhoomkar/yc-startups-context/blob/main/README.md)
- [Base dataset metadata](https://github.com/yashbhoomkar/yc-startups-context/blob/main/data/metadata.json)
- [Derived enrichment metadata](https://github.com/yashbhoomkar/yc-startups-context/blob/main/data/enrichment_metadata.json)
- [Verified enrichment records](https://github.com/yashbhoomkar/yc-startups-context/blob/main/data/verified_enrichment.csv)
- [Dataset build script](https://github.com/yashbhoomkar/yc-startups-context/blob/main/scripts/build_dataset.py)
- [Enrichment script](https://github.com/yashbhoomkar/yc-startups-context/blob/main/scripts/enrich_dataset.py)
- [YC public company directory](https://www.ycombinator.com/companies/)
- [Community-maintained YC OSS API](https://github.com/yc-oss/api)
