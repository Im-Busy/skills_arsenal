# Source Credibility Tiers — Phase 0 Filtering

Phase 0 (FIND) searches broadly, downloads generously, but filters ruthlessly. The
5-tier classification system below determines which sources are credible enough to
keep for the current project. **Only tiers 1–4 pass; tier 5 sources are deleted
immediately.**

The goal is not to maximize volume — it is to ensure every kept document meets a
minimum credibility bar so downstream phases (CLASSIFY, EVALUATE, CONFLICT-RESOLVE,
SYNTHESIZE, ARCHITECT) operate on defensible evidence. False positives (keeping a
bad source) waste downstream effort. False negatives (deleting a good source) are
safer — the search can be re-run with broader terms.

## Tier Definitions

| Tier | Label | Source Types | Examples | Trust Level |
|------|-------|-------------|----------|-------------|
| 1 | **Authoritative** | Professional bodies, standards organizations | CFA Institute, IEEE, ISO, NIST, IETF, W3C | Highest — cite with confidence |
| 2 | **Official** | Government agencies, regulators, major institutions | SEC, Federal Reserve, BIS, IMF, .gov domains, European Commission | High — official data/standards |
| 3 | **Professional** | Major consulting firms, Big 4, established research orgs | McKinsey, Deloitte, PwC, EY, KPMG, BCG, Bain, RAND, Brookings | Moderate-High — methodology varies |
| 4 | **Academic** | Established journals, university presses, highly-cited papers | Nature, Science, arXiv (≥50 citations), university .edu domains | Moderate — peer review quality varies |
| 5 | **Unverified** | Blogs, personal sites, marketing content, student papers, social media | Medium, Substack (unverified author), undergraduate theses | Low — DELETE in Phase 0 filter |

### Tier 1 — Authoritative (detailed)

Sources that set the standard in their domain. Standards bodies publish
specifications after multi-stakeholder consensus processes. Professional bodies
enforce codes of ethics and peer review. Documents from these sources can be cited
directly without additional validation. Example use: citing an IEEE standard for
network protocols or a CFA Institute research paper on portfolio risk.

### Tier 2 — Official (detailed)

Government and regulatory data is the primary source for market statistics,
economic indicators, legal frameworks, and policy analysis. `.gov` and `.gov.hk`
domains are always tier 2 unless the specific page is a personal blog hosted on a
subdomain. International bodies like the IMF and BIS fall here because their
member-state governance gives their data quasi-official status.

### Tier 3 — Professional (detailed)

Consulting firms and established research organizations produce high-quality
analysis but may have commercial or advocacy angles. A McKinsey report on industry
trends is valuable; a McKinsey pitch deck for a client engagement is marketing.
The key discriminator: does the document present data, methodology, and sources,
or does it only assert conclusions? The former is keep-worthy; the latter is
filtered out by the decision rules below.

### Tier 4 — Academic (detailed)

Peer-reviewed journals provide the gold standard for academic rigor, but review
quality varies significantly. Conference proceedings are tier 4 unless the venue
is top-tier (see Special Cases). Preprints increase the risk of unvalidated
claims — citation count is used as a proxy for community vetting. University .edu
domains are tier 4 by default, but student project pages and personal faculty
blogs may be tier 5 (evaluate by content, not domain).

### Tier 5 — Unverified (detailed)

No barrier to publication. Medium posts, Substack newsletters, personal blogs,
and undergraduate theses have minimal quality assurance. A tier 5 source may
contain correct information, but the cost of verifying it outweighs the value —
the same information can almost always be found in a tier 1–4 source. Delete
without exception.

## Filter Decision Rules

Rules are evaluated in order. The first matching rule wins.

```
IF tier 5 → DELETE (regardless of content quality)
  Rationale: No verification path. The agent would need to independently confirm
  every claim, which is more expensive than searching for an equivalent tier 1-4
  source.

IF tier 4 AND <500 chars extractable text → DELETE
  Rationale: A conference abstract or short paper with under 500 characters of
  actual content has insufficient substance for analysis. The extractor may have
  failed — but the document is still not useful in this state.

IF tier 3 AND clearly marketing material (no data/methodology) → DELETE
  Rationale: Professional tier documents that assert conclusions without showing
  data sources, sample sizes, methodology, or statistical rigor are promotional,
  not analytical. Indicators: "we believe", "our proprietary approach", no
  bibliography, no data tables.

IF tier 2 AND >10 years old → KEEP (flag as potentially outdated)
  Rationale: Official data can be historically valuable (e.g., SEC filings from
  2010 may inform a trend analysis). The flag alerts downstream phases to check
  currency. The document is NOT deleted.

All other cases → KEEP
  Rationale: Default to inclusion. The downstream phases (EVALUATE, SYNTHESIZE)
  will further scrutinize and weight sources. Phase 0 is a coarse filter, not a
  final judge.
```

## Special Cases

These override the default tier assignment for ambiguous source types.

### Open-source project READMEs

README files document tool capabilities, installation, and usage. They are a
primary source for understanding what a tool does, but quality varies with
project maturity.

| Condition | Tier | Rationale |
|-----------|:----:|----------|
| ≥100 GitHub stars | 3 | Community vetting, active maintenance |
| 10–99 stars | 4 | Some community interest, may be abandoned |
| <10 stars | 5 | Personal project, no community validation |

### Preprints (arXiv, SSRN, bioRxiv)

Preprints have not passed peer review. Citation count proxies community attention.

| Condition | Tier | Rationale |
|-----------|:----:|----------|
| ≥50 citations | 3 | Significant community uptake, likely influential |
| <50 citations | 4 | Unvalidated but potentially useful; flag as preprint |

### Conference proceedings

Conference quality varies enormously. Use csrankings.org for computer science
and Google Scholar Metrics for other fields.

- **Top-tier venue** (top 20% per csrankings.org) → tier 3
- **All other venues** → tier 4
- **Predatory conferences** (check Beall's list) → tier 5, DELETE

### Industry white papers

- From a recognized company (FAANG, Microsoft, top AI labs, established vendors)
  or research lab (e.g., DeepMind, MSR, FAIR) → tier 3
- From an unknown startup or individual consultant → tier 5, DELETE
- If in doubt, check the company's Crunchbase or LinkedIn: <50 employees and
  <5 years old → unknown startup

### Wikipedia

Wikipedia is a starting point for discovering primary sources. It must never be
cited directly. The Phase 0 workflow:

1. Read the Wikipedia article → tier 4
2. Collect the primary sources cited in the footnotes
3. Classify each primary source independently using these tiers
4. Delete the Wikipedia article from the kept set
5. Keep only the re-classified primary sources

**Exception:** If the Wikipedia article is the only available source and the
project scope permits (e.g., broad landscape survey), keep as tier 4, but flag
prominently.

### Books and textbooks

- Published by academic press (Oxford, Cambridge, MIT, Pearson, O'Reilly) → tier 3
- Published by trade press (Wiley, Apress, Manning) → tier 4
- Self-published → tier 5, DELETE

### News articles

- Major outlets (Reuters, Bloomberg, WSJ, FT, AP) → tier 3
- Established outlets (NYT, WaPo, The Economist) → tier 4 (editorial bias possible)
- Unverified outlets (Medium, Substack news, unknown blogs) → tier 5, DELETE

## Phase 0 Output

After filtering the downloaded batch, the researcher produces a structured listing.

### Kept documents

Documents that pass filtering are listed in `research-output/README.md` with:

- File name and path (relative to `research-output/`)
- Assigned tier (1–4)
- Brief justification (e.g., "Tier 2 — SEC filing, official regulatory data")
- Date of publication
- Estimated extractable character count
- Any flags (e.g., "potentially outdated — >10 years old")

Format example:

```markdown
| File | Tier | Justification | Date | Chars | Flags |
|------|:----:|---------------|:----:|:-----:|-------|
| sec-10k-2023.md | 2 | SEC filing — official regulatory data | 2023-11-01 | 48,200 | — |
| mckinsey-ai-report.md | 3 | Professional consulting report with methodology | 2024-02-15 | 12,400 | — |
| fed-interest-rate.md | 2 | Federal Reserve official statement | 2010-06-20 | 3,100 | ⚠ >10 years old |
```

### Deleted documents

Deleted documents are listed with the deletion reason for auditability:

```markdown
| File | Reason |
|------|--------|
| medium-blog-post.md | Tier 5 — unverified source, deleted |
| conf-abstract.md | Tier 4 — <500 chars extractable text, deleted |
| startup-whitepaper.md | Tier 5 — unknown startup, deleted |
```

### Gate check

The `verify_gates.py --phase=find` check enforces:

1. **`research-output/README.md` exists** — filtering was completed
2. **≥1 document survived filtering** — search was productive
3. **No tier 5 documents remain** — filtering was correctly applied

If all documents are deleted, Phase 0 must be re-run with broader search terms,
different search engines, or adjusted date ranges. Do NOT lower the tier
threshold — maintaining credibility is non-negotiable.