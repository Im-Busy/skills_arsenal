# Note Schema — JSONL Field Definitions

The research-investigation pipeline produces structured notes in **JSONL** (JSON Lines) format — one JSON object per line. JSONL is the **working format**: each line is a self-contained record that can be queried with `jq`, counted with `wc -l`, validated independently, and piped between phases. The **output format** is Markdown (synthesis reports, insight summaries). JSONL is always the intermediate representation.

Three phases produce entries: **SCAN** (Phase 1), **DEEP-READ** (Phase 2), and **CROSS-CONNECT** (Phase 3). Each entry type has its own schema, validation rules, and role in the pipeline.

---

## Phase 1 — SCAN Entries

Every page of every source document receives exactly one SCAN entry. The scan identifies sections worth deep-reading.

```json
{
  "id": "<doc>_p<page>",
  "doc": "<source-filename>",
  "page": <int>,
  "section": "<section-heading>",
  "phase": "scan",
  "summary": "<1-sentence summary>",
  "signal": "high|medium|low",
  "tags": ["<tag1>", "<tag2>"]
}
```

| Field | Type | Rules |
|-------|------|-------|
| `id` | string | Format `<docname>_p<page_number>`. Example: `paper-a_p3`. Must be unique per line. |
| `doc` | string | Source filename, e.g., `paper-a.md`. Matches `doc` field of the originating source entry. |
| `page` | int | Integer page number from the source. 1-based. |
| `section` | string | Section heading verbatim from the document, e.g., `2.1 Methodology`. Use `"N/A"` if no heading. |
| `phase` | string | Always `"scan"`. |
| `summary` | string | **ONE substantive sentence.** Must capture the actual claim, finding, or content. Not "This page talks about X" — state *what* it says. |
| `signal` | string | `high` = key finding, methodology, or central claim. `medium` = supporting content, context, examples. `low` = boilerplate, acknowledgments, table of contents, references list. |
| `tags` | array[str] | 0–5 keywords. Lowercase, hyphenated. Example: `["compression","pipeline","architecture"]`. Empty array allowed. |

### Scan Signal Rules

| Signal | Meaning | Typical Sections | Triggers Deep-Read? |
|--------|---------|------------------|---------------------|
| `high` | Core finding or method | Methodology, Results, Key Claims | Yes — must get a DEEP-READ entry |
| `medium` | Supporting evidence | Related Work, Background, Discussion | Optional — agent discretion |
| `low` | Structural | Acknowledgments, References, TOC | No — skipped |

---

## Phase 2 — DEEP-READ Entries

Deep-read entries extract a single **falsifiable claim** from a page identified as `signal=high` (or `medium` at agent discretion). Each claim gets its own entry. A single page may produce multiple entries if it contains multiple claims.

```json
{
  "id": "insight_NNN",
  "doc": "<source-filename>",
  "page": <int>,
  "section": "<section>",
  "phase": "deep-read",
  "key_claim": "<main finding>",
  "evidence_type": "benchmark|case_study|argument|citation|assertion",
  "evidence_detail": "<brief description>",
  "strength": "strong|moderate|weak",
  "strength_justification": "<why>",
  "quality_scores": {
    "testability": 0.8,
    "falsifiability": 0.6,
    "parsimony": 0.7,
    "explanatory_power": 0.9,
    "scope": 0.5,
    "consistency": 0.8,
    "novelty": 0.7
  },
  "builds_on": [],
  "contradicts": [],
  "extends": [],
  "parallels": [],
  "gaps": "<what's missing>",
  "confidence": 0.85
}
```

| Field | Type | Rules |
|-------|------|-------|
| `id` | string | Format `insight_NNN` (zero-padded to 3 digits). Example: `insight_007`. Sequential across all sources. |
| `doc` | string | Source filename — links back to the originating SCAN entry. |
| `page` | int | Page number where the claim appears. Matches a SCAN entry's page. |
| `section` | string | Section heading — copied from the corresponding SCAN entry. |
| `phase` | string | Always `"deep-read"`. |
| `key_claim` | string | **One sentence.** A falsifiable claim — something that could be proven wrong. Not a description. Example: "Pre-execution rewrite reduces token consumption by 73% on CI output." Bad: "This section discusses token reduction." |
| `evidence_type` | enum | One of: `benchmark` (measured, reproducible), `case_study` (real-world example), `argument` (logical reasoning), `citation` (references external work), `assertion` (stated without evidence). |
| `evidence_detail` | string | Brief description: what was measured, what study, what dataset. One sentence max. |
| `strength` | enum | `strong` = well-evidenced (benchmark + replication). `moderate` = some evidence, clear gaps. `weak` = mostly assertion or single anecdote. |
| `strength_justification` | string | WHY this rating. Cite evidence gaps, missing controls, or corroboration from other sources. |
| `quality_scores` | object | 7 axes, each 0.0–1.0. See `quality-criteria.md` for full definitions. |
| `builds_on` | array[str] | IDs of insights it directly depends on. Empty `[]` if none yet. |
| `contradicts` | array[str] | IDs of insights it directly conflicts with. Empty `[]` if none yet. |
| `extends` | array[str] | IDs of insights it generalizes. Empty `[]` if none yet. |
| `parallels` | array[str] | IDs of insights that independently reached the same finding. Empty `[]` if none yet. |
| `gaps` | string | What's missing, assumed, or untested. What would a skeptic ask? One sentence. |
| `confidence` | float | Composite 0.0–1.0. **Default** = mean of `quality_scores`. **Adjustments**: +0.1 for `benchmark` evidence, −0.1 for `assertion`. Clamped to [0.0, 1.0]. |

### Quality Score Axes (0.0–1.0)

| Axis | Definition |
|------|-----------|
| `testability` | Can the claim be empirically tested? |
| `falsifiability` | Could evidence disprove it? |
| `parsimony` | Does it avoid unnecessary assumptions (Occam)? |
| `explanatory_power` | How much does it explain? |
| `scope` | How widely does it apply? |
| `consistency` | Does it agree with established knowledge? |
| `novelty` | How surprising or new is it? |

---

## Phase 3 — CROSS-CONNECT Entries

Cross-connect entries pair two DEEP-READ insights and classify their relationship. Every pair must be evaluated; only non-trivial connections are recorded.

```json
{
  "id": "conn_NNN",
  "phase": "cross-connect",
  "type": "compounds",
  "insight_a": "insight_007",
  "insight_b": "insight_014",
  "mechanism": "Pre-execution rewrite reduces command output, making post-execution compression more effective",
  "formula_score": 0.82,
  "council_votes": {
    "empiricist": 0.9,
    "synthesizer": 0.85,
    "contrarian": 0.6,
    "architect": 0.8,
    "statistician": 0.75
  },
  "council_verdict": "confirmed",
  "confidence": 0.78
}
```

| Field | Type | Rules |
|-------|------|-------|
| `id` | string | Format `conn_NNN`. Example: `conn_012`. Sequential across all connections. |
| `phase` | string | Always `"cross-connect"`. |
| `type` | enum | One of: `builds_on` (B depends on A), `contradicts` (A and B conflict), `extends` (B generalizes A), `parallels` (independent same finding), `compounds` (A makes B more effective — true synergy). |
| `insight_a` | string | A Phase 2 insight ID. The reference/"prior" insight in directional relationships. |
| `insight_b` | string | A Phase 2 insight ID. The dependent/succeeding insight. |
| `mechanism` | string | **1–2 sentences** describing HOW they connect. Must be specific: name the mechanism, not just "they are related." |
| `formula_score` | float | Output of the synergy formula (see `synergy-formula.md`). 0.0–1.0. |
| `council_votes` | object | 5 persona keys, each 0.0–1.0. 4 core + 1 specialist (the specialist varies by domain — see `council-config.md`). |
| `council_verdict` | enum | `confirmed` (mean ≥ 0.7), `disputed` (0.4–0.7), `rejected` (mean < 0.4). |
| `confidence` | float | Mean of `council_votes`. |

### Connection Types

| Type | Description | Example |
|------|-------------|---------|
| `builds_on` | B assumes or requires A's finding | Insight_007's compression technique requires Insight_014's dedup pass first |
| `contradicts` | A and B make incompatible claims | Insight_007 claims 73% savings, Insight_014 reports 12% on same dataset |
| `extends` | B operates in a broader context of A's domain | Insight_014 applies Insight_007's method to multi-file repos |
| `parallels` | Independent sources converged on same finding | Both papers report ~70% compression on CI output |
| `compounds` | A makes B more effective — multiplicative synergy | Pre-execution rewrite (A) removes noise, making compression (B) converge faster |

---

## Validation Rules

The script `verify_gates.py` checks each phase's output against these rules before the pipeline proceeds to the next phase.

### Phase 1 Gate (SCAN)

- Count of SCAN entries ≥ 0.8 × total pages across all source documents
- Every SCAN entry has all required fields non-empty
- Every `id` is unique and matches pattern `<docname>_p<digits>`
- Every `signal` is one of `high`, `medium`, `low`
- No duplicate `doc` + `page` combinations

### Phase 2 Gate (DEEP-READ)

- Count of DEEP-READ entries ≥ 5
- All required fields non-empty (strings non-empty, arrays present, scores present)
- All `confidence` ≥ 0.3
- All `id` values match pattern `insight_NNN`
- Every `key_claim` is ≥ 10 characters (guards against placeholder text)
- Every `evidence_type` is a valid enum value
- Every `quality_scores` object has all 7 axes

### Phase 3 Gate (CROSS-CONNECT)

- ≥ 3 distinct connection types present
- ≥ 1 connection of type `compounds`
- ≥ 1 connection of type `contradicts` OR every pair is confirmed by Council as "no conflicts"
- All `insight_a` and `insight_b` values reference existing DEEP-READ IDs
- All `formula_score` values in [0.0, 1.0]
- All `council_verdict` values are valid enum
- No duplicate pairs (same `insight_a` + `insight_b` combination)

---

## Cross-Phase References

The three phases chain together through these reference patterns:

```
SCAN ────signal=high────► DEEP-READ
                            │
                            │ insight_a / insight_b
                            ▼
                       CROSS-CONNECT
                            │
                            │ all entries
                            ▼
                       SYNTHESIS (Phase 4)
```

### Reference Chain

| Phase | Entry ID Pattern | Referenced By | How |
|-------|-----------------|---------------|-----|
| **SCAN** | `<doc>_p<N>` | Phase 2 `doc`+`page` | `signal=high` entries are candidates for deep-reading |
| **DEEP-READ** | `insight_NNN` | Phase 3 `insight_a`, `insight_b` | Cross-connect pairs reference exactly two insights |
| **CROSS-CONNECT** | `conn_NNN` | Phase 4 synthesis | All connections feed into the final synthesis report |

### Integrity Rules

- Every `doc` field in a DEEP-READ entry must have at least one corresponding SCAN entry with matching `doc` and `page`.
- Every `insight_a`/`insight_b` in a CROSS-CONNECT entry must exist as a DEEP-READ entry `id`.
- Orphan references (entries referencing non-existent IDs) cause pipeline failure.
- The reference chain is strictly linear: SCAN → DEEP-READ → CROSS-CONNECT → SYNTHESIS. Skip-phase references are not allowed.