---
name: research-investigation
description: >
  Analyzes materials already held page by page, extracts structured insights,
  connects findings, and produces synthesis reports with mandatory visual
  diagrams. Hybrid invocation — activates on context match or when the LLM
  identifies relevance at any point. Use when the user asks to investigate or
  synthesize held PDFs, papers, markdown, web pages, transcripts, or technical
  documents. Do NOT confuse with `directed-document-research`, which finds,
  downloads, and filters web documents. Do NOT use for document gathering alone,
  reading a single short document, general Q&A without document review, or
  code-only exploration without prose materials.
license: MIT
metadata:
  version: "0.1.0"
  skill-author: project
  invocation_posture: hybrid
---

# research-investigation

## Overview

The research-investigation skill is a **7-phase pipeline** for AI agents to systematically investigate research materials page-by-page, extract structured insights, find synergies between findings, and produce synthesis reports with mandatory visual diagrams.

## Related skills / Do NOT confuse with

- **Do NOT confuse with `directed-document-research`.** Use this skill for page-by-page analysis and synthesis of materials already held. Use `directed-document-research` to find, download, filter, and store web documents; Phase 0 may call it as a secondary acquisition step.

```
Phase 0: FIND      →  Phase 1: SCAN      →  Phase 2: DEEP-READ
                                        ↘              ↘
                                    Phase 3: CROSS-CONNECT
                                        ↓
                                    Phase 4: SYNTHESIZE
                                        ↓
                                    Phase 5: REPORT
```

### Key Principles

- **Phase gates are automated** — every phase has a gate (`verify_gates.py`) that must return **PASS** before the agent proceeds. The agent **cannot** skip or ignore a failing gate.
- **Visual elements are mandatory** — 4 visuals generated at phase transitions (coverage heatmap, insight scatterplot, connection graph, synthesis dashboard). No report is complete without all four.
- **JSONL is the working format** — all structured data flows through `insights.jsonl` as newline-delimited JSON records with typed schemas per phase. Markdown is the output format only.
- **Council uses real delegation** — Phase 3 spawns 5 parallel subagents with distinct personas. Each votes independently; votes are aggregated numerically.
- **Portability** — follows Agent Skills standard for multi-host deployment. Self-contained; reference files loaded on demand from `references/`.
- **Phase 0 is optional** — when source materials are missing, delegate the search/download/convert/filter workflow to `directed-document-research` before synthesis.

## When to Use

**Trigger phrases — hybrid invocation activates on any of these:**
- "Investigate these documents"
- "Analyze these papers page by page"
- "Extract insights from these materials"
- "What do these documents tell us?"
- "Find connections between these findings"
- "How do these papers relate?"
- "Synthesize findings from these sources"
- "Systematically study and report on..."

**Do NOT use for:**
- Finding documents (Phase 0 handles this internally via `directed-document-research`)
- Reading a single short document (use direct read tools instead)
- General Q&A without document review
- Code-only exploration without prose materials

---

## Phase 0: FIND (optional; delegated to `directed-document-research`)

**Goal:** When source materials are missing, discover, download, and curate them before investigation.

Skip this phase when the materials already exist. Otherwise, delegate to the `directed-document-research` skill. The full process is defined there; this is a summary of what it produces and what the agent must verify.

### Process
1. **Multi-angle search** — search web, academic databases, and known sources for relevant documents
2. **Batch download** — fetch all candidate PDFs and web pages
3. **Convert** — PDFs → markdown using `marker` or equivalent
4. **Ruthless relevance filter** — discard documents that don't directly address the research question. Keep only what passes source credibility tiers (see `references/source-credibility-tiers.md`).

### Output
```
research-output/
├── doc1.md
├── doc2.md
├── doc3.md
└── README.md              # Documents kept, sources, credibility tiers
```

### Gate
```
verify_gates.py --phase=find --input research-output/
```
- All kept documents are valid markdown with ≥1 heading
- README.md exists with document list and source metadata
- No document is shorter than 100 words unless it's a supplementary resource

### Phase Transition Visual
None — Phase 0 is absorbed from `directed-document-research`. The first visual is generated after Phase 1.

---

## Phase 1: SCAN

**Goal:** Read EVERY page of EVERY document. Extract 1-sentence summaries + signal tags.

### Process

1. **For each document**, identify page/section boundaries (headings, page breaks, logical chunks)
2. **Read each page**, extract exactly 1 sentence summarizing the page's core content
3. **Assign signal**: `high` (key finding / methodology / claim), `medium` (supporting context / examples), `low` (boilerplate / table of contents / navigation)
4. **Add 0-5 keyword tags** representing the page's topics
5. **Write each page as a JSONL scan entry** using the schema below

### JSONL Format (scan entry)

```json
{
  "id": "<doc>_p<page>",
  "doc": "<filename>",
  "page": <int>,
  "section": "<heading>",
  "phase": "scan",
  "summary": "<1-sentence summary>",
  "signal": "high|medium|low",
  "tags": ["tag1", "tag2"]
}
```

Load `references/note-schema.md` before beginning this phase for full field specifications.

### Gate
```
verify_gates.py --phase=scan --input research-output/insights.jsonl --doc-pages doc1:N --doc-pages doc2:M
```
- **≥80% page coverage** across all documents combined
- Every document has at least 1 scan entry
- All entries have valid `signal` values and non-empty `summary`
- No duplicate page IDs within same document

### Phase Transition Visual (mandatory)
**Coverage heatmap** — produce `research-output/visuals/coverage-heatmap.png`:
- Rows = documents
- Columns = page ranges
- Color = signal (green=high, yellow=medium, red=low)
- White = unscanned (must be <20% of total cells)

See `references/diagramming-guide.md` for implementation templates.

---

## Phase 2: DEEP-READ

**Goal:** Revisit high-signal pages and extract structured insights with quality scoring.

### Process

1. **Select pages to deep-read:**
   - All pages with `signal=high` from Phase 1 entries
   - Any page in a section where ≥50% of pages are `signal=medium`
2. **For each selected page**, re-read the full section and extract a structured insight using the complete template below
3. **Score on 7 quality axes** (see `references/quality-criteria.md`):
   - `testability` — can this claim be tested empirically?
   - `falsifiability` — could evidence disprove it?
   - `parsimony` — is it the simplest explanation?
   - `explanatory_power` — how much does it explain?
   - `scope` — how broadly does it apply?
   - `consistency` — does it contradict known facts?
   - `novelty` — is it surprising or new?
4. **Compute confidence** = mean of all 7 quality scores, adjusted ±0.1 if evidence has internal contradictions
5. **Populate relationship arrays** (`builds_on`, `contradicts`, `extends`, `parallels`) — these can be empty initially; Phase 3 fills them

### JSONL Format (deep-read entry)

```json
{
  "id": "insight_NNN",
  "doc": "<filename>",
  "page": <int>,
  "section": "<heading>",
  "phase": "deep-read",
  "key_claim": "<concise statement of the claim>",
  "evidence_type": "benchmark|case_study|argument|citation|assertion",
  "evidence_detail": "<supporting detail or quote>",
  "strength": "strong|moderate|weak",
  "strength_justification": "<why this strength rating>",
  "quality_scores": {
    "testability": <0.0-1.0>,
    "falsifiability": <0.0-1.0>,
    "parsimony": <0.0-1.0>,
    "explanatory_power": <0.0-1.0>,
    "scope": <0.0-1.0>,
    "consistency": <0.0-1.0>,
    "novelty": <0.0-1.0>
  },
  "builds_on": [],
  "contradicts": [],
  "extends": [],
  "parallels": [],
  "gaps": "<what's missing or uncertain>",
  "confidence": <float 0.0-1.0>
}
```

Load `references/quality-criteria.md` before beginning this phase.

### Gate
```
verify_gates.py --phase=deep-read --input research-output/insights.jsonl
```
- **≥5 insights** (or min(5, total_pages / 3), whichever is smaller)
- All required fields populated with non-null values
- All `confidence` values ≥ 0.3
- `quality_scores` contains all 7 axes for every entry

### Phase Transition Visual (mandatory)
**Insight scatterplot** — produce `research-output/visuals/insight-scatter.png`:
- X-axis = novelty score
- Y-axis = confidence
- Point size = scope score (scaled)
- Color = evidence type
- Annotated with insight IDs for outliers

See `references/diagramming-guide.md` for implementation templates.

---

## Phase 3: CROSS-CONNECT

**Goal:** Find synergies, conflicts, and patterns between insights using formula scoring + multi-agent Council review.

### Process

1. **Formula scoring** — Score EVERY pair of insights using the synergy formula from `references/synergy-formula.md`:
   - Computes pair compatibility based on shared tags, complementary evidence types, and non-overlapping quality profiles
   - Output: a float `formula_score` per pair (0.0-1.0)
2. **Filter** — Select the top 30% of scoring pairs. If total pairs < 5, send ALL pairs regardless.
3. **Council** — Spawn 5 parallel subagents with distinct personas (see `references/council-archetypes.md`):
   - **Core 4 (always spawned):**
     - **Empiricist** — evaluates evidence quality and testability
     - **Synthesizer** — looks for connecting narratives and patterns
     - **Contrarian** — actively seeks flaws and alternative explanations
     - **Architect** — evaluates structural fit and system-level implications
   - **+1 Specialist (selected by decision tree):**
     - Statistician — if formula scores have high variance
     - Security Auditor — if insights involve security, privacy, or access control
     - Domain Expert — if all insights are from one narrow subdomain
     - Ethicist — if insights involve human subjects, bias, or fairness
     - Generalist — default when no specialist trigger matches
4. **Aggregate** — For each pair, collect each Council member's vote (0.0-1.0):
   - `confirmed` — mean ≥ 0.7
   - `disputed` — mean between 0.4 and 0.7
   - `rejected` — mean < 0.4
5. **Determine connection type** for each confirmed pair:
   - `builds_on` — insight A provides foundation for insight B
   - `contradicts` — insights disagree on a shared claim
   - `extends` — insight A applies to a broader scope
   - `parallels` — insights reach similar conclusions independently
   - `compounds` — insights together produce a non-obvious synergy greater than the sum

### JSONL Format (connection entry)

```json
{
  "id": "conn_NNN",
  "phase": "cross-connect",
  "type": "builds_on|contradicts|extends|parallels|compounds",
  "insight_a": "insight_NNN",
  "insight_b": "insight_NNN",
  "mechanism": "<description of how they relate>",
  "formula_score": <float>,
  "council_votes": {
    "empiricist": <float>,
    "synthesizer": <float>,
    "contrarian": <float>,
    "architect": <float>,
    "<specialist>": <float>
  },
  "council_verdict": "confirmed|disputed|rejected",
  "confidence": <float>
}
```

Load `references/synergy-formula.md` and `references/council-archetypes.md` before this phase.

### Gate
```
verify_gates.py --phase=cross-connect --input research-output/insights.jsonl
```
- **≥3 distinct connection types** (e.g., compounds + builds_on + contradicts)
- **≥1 `compounds`** type (true synergy, not just similarity)
- **≥1 `contradicts`** type, OR Council-confirmed no genuine conflicts exist (documented)

### Phase Transition Visual (mandatory)
**Connection graph** — produce `research-output/visuals/connection-graph.png`:
- Nodes = insight IDs, sized by confidence
- Edges = connections, colored by type
- Layout = force-directed or hierarchical
- Legend for edge types and node sizes

See `references/diagramming-guide.md` for implementation templates.

---

## Phase 4: SYNTHESIZE

**Goal:** Produce a unified synthesis with 4 mandatory sections that distills all findings into actionable intelligence.

### Process

1. **Review all insights** (Phase 2 entries) and **connections** (Phase 3 entries) in `insights.jsonl`
2. **Write 4 sections** using the synthesis format template from `references/synthesis-format.md`:
   - **Points of Convergence** — where multiple independent insights agree. Identify ≥2 convergence themes with supporting evidence.
   - **Core Tension** — the central disagreement or paradox revealed by the research. Often the single most valuable finding. If no contradictions exist, state what the literature takes for granted.
   - **The Blind Spot** — what NO source addressed. A gap that emerged from cross-document comparison. If genuinely nothing is missing, state that explicitly.
   - **Recommended Actions** — ≥3 concrete actions ordered by priority. Each action must cite at least one insight ID and be specific enough to execute.
3. **Embed** this synthesis in `research-output/report.md`

Load `references/synthesis-format.md` before beginning this phase.

### Gate
```
verify_gates.py --phase=synthesize --synthesis-file research-output/report.md
```
- All 4 sections present with ≥2 sentences each
- ≥3 recommended actions with cited insight IDs
- Each action includes a concrete next step, not just a principle

### Phase Transition Visual (mandatory)
**Synthesis dashboard** — produce `research-output/visuals/synthesis-dashboard.png`:
- 2×2 grid or single-page layout showing all 4 synthesis sections as panels
- Points of Convergence as a stacked bar or Venn overlay
- Core Tension as a comparison bar (pro/con evidence counts)
- Blind Spot as a highlighted gap annotation
- Recommended Actions as a priority-ordered list with impact estimates

See `references/diagramming-guide.md` for implementation templates.

---

## Phase 5: REPORT

**Goal:** Generate the final output with all artifacts assembled.

### Process

1. **Run the report generator:**
   ```
   jsonl_to_markdown.py --input research-output/insights.jsonl --output research-output/report.md
   ```
   This renders the full synthesis report from the JSONL database, embedding the synthesis sections written in Phase 4.

2. **Verify all 4 visuals exist** in `research-output/visuals/`:
   - `coverage-heatmap.png`
   - `insight-scatter.png`
   - `connection-graph.png`
   - `synthesis-dashboard.png`

3. **Generate README.md** executive summary at `research-output/README.md`:
   - Documents investigated (count and names)
   - Total insights extracted
   - Key connections found (counts per type)
   - Top 3 findings (most confident insights)
   - Visual gallery (embedded thumbnails with links)

### Output Structure
```
research-output/
├── report.md              # Full synthesis report
├── insights.jsonl         # Complete insight database (all phases)
├── visuals/
│   ├── coverage-heatmap.png
│   ├── insight-scatter.png
│   ├── connection-graph.png
│   └── synthesis-dashboard.png
└── README.md              # Executive summary
```

### Gate
```
verify_gates.py --phase=report --input research-output/
```
- All 5 output files present
- `report.md` is valid markdown with ≥1 heading
- `insights.jsonl` contains entries from phases 1, 2, and 3
- All 4 visuals exist and are valid image files
- README.md contains executive summary

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Skip to synthesis without completing Phase 1 scan | Run full scan (Phase 1) — scanning reveals structure you'll miss |
| Extract insights from only the first document | Cover ALL documents with scan entries before deep-reading |
| Accept `verify_gates.py` FAIL and proceed anyway | Fix the violations. The gate is there for a reason |
| Score insight quality without reading the full page | Read the complete page/section before assigning quality scores |
| Use default 0.5 for quality scores when uncertain | Score 0.0 if the source doesn't address the axis |
| Generate complex visuals for trivial documents | Minimal visuals are valid — 2-cell heatmap, 1-point scatterplot |
| Run Council review on all insight pairs | Formula filters top 30%. Only Council-review the best candidates |
| Combine percentages from different token types | Each insight's confidence is independent. Don't average them |
| Edit insights.jsonl by hand | Use scripted updates or append-only writes. JSONL is a machine format |
| Re-read documents after Phase 1 | Trust your scan summaries. Re-read only for Deep-Read selected pages |
| Defer visual generation to "the end" | Generate at each phase transition as specified. Proves each phase completed |

---

## Example Session

```
User: "Investigate these 3 PDFs about compression techniques"

Agent flow:
1. Phase 0 (FIND): Searches for compression papers, downloads 3 PDFs,
   converts to markdown, filters to 3 kept docs.
   Gate: verify_gates.py --phase=find → PASS.

2. Phase 1 (SCAN): Reads all pages (75 total), produces 75 scan entries
   with summaries and signal tags. Coverage: 83%.
   Gate: verify_gates.py --phase=scan --doc-pages doc1:25 doc2:30 doc3:20 → PASS.
   Visual: coverage-heatmap.png (3 docs × 25+30+20 pages, green/yellow/red cells).

3. Phase 2 (DEEP-READ): Selects 22 high-signal pages, extracts 22 structured
   insights. All 7 quality axes scored. Confidence range: 0.31-0.89.
   Gate: verify_gates.py --phase=deep-read → PASS (≥5 insights, all ≥0.3).
   Visual: insight-scatter.png (22 points, novelty×confidence, colored by evidence type).

4. Phase 3 (CROSS-CONNECT): Scores 231 pairs (22×21/2), top 69 advance to
   Council. 5 parallel subagents evaluate. Produces 34 connections:
   8 compounds, 12 builds-on, 6 extends, 5 parallels, 3 contradicts.
   Gate: verify_gates.py --phase=cross-connect → PASS.
   Visual: connection-graph.png (nodes=insights, edges=connections by type).

5. Phase 4 (SYNTHESIZE): Writes Convergence (3 themes — frequency-domain,
   dictionary-based, learned compression all converge on entropy models),
   Core Tension (pre-execution vs post-execution compression tradeoffs),
   Blind Spot (no GPU benchmark studies found),
   Actions (6 recommendations with cited insight IDs).
   Gate: verify_gates.py --phase=synthesize → PASS.
   Visual: synthesis-dashboard.png (4-panel dashboard).

6. Phase 5 (REPORT): Runs jsonl_to_markdown.py, verifies all 4 visuals,
   generates README.md executive summary.
   Gate: verify_gates.py --phase=report → PASS. Done.
```

Total pipeline: ~15-30 minutes agent time for 3 documents, 75 pages.

---

## References

Load these files on demand at the specified phase. All paths are relative to this skill's directory.

| Reference File | Load Before | Purpose |
|----------------|-------------|---------|
| `references/note-schema.md` | Phase 1 | Full JSONL field definitions, types, constraints |
| `references/quality-criteria.md` | Phase 2 | 7-axis scoring rubric with examples for each axis |
| `references/synergy-formula.md` | Phase 3 | Pair scoring formula with weight matrices and normalization |
| `references/synthesis-format.md` | Phase 4 | 4-section output template with example prose |
| `references/council-archetypes.md` | Phase 3 (Council) | 9 persona definitions, selection decision tree, voting protocol |
| `references/diagramming-guide.md` | Every phase transition | Visual templates for all 4 mandatory visuals (matplotlib/Python) |
| `references/source-credibility-tiers.md` | Phase 0 | Tier definitions (Tier 1-4) for source filtering |
| `scripts/verify_gates.py` | Every phase transition | Phase gate checker — run with phase flag and input path |
| `scripts/jsonl_to_markdown.py` | Phase 5 | Report generator that renders insights.jsonl to report.md |
| `scripts/merge_sessions.py` | Cross-session | Merge multiple insight databases from parallel investigation sessions |

---

## Integration Notes

- **Phase 0 absorption**: This skill delegates document discovery to `directed-document-research`. When triggered with documents already present (e.g., "investigate these files"), skip Phase 0 and start at Phase 1. When triggered without documents (e.g., "find and analyze papers about X"), load `directed-document-research` for Phase 0, then continue the pipeline.

- **Cross-session merging**: For large-scale investigations, split across multiple agent sessions. Use `scripts/merge_sessions.py` to combine `insights.jsonl` files from parallel sessions, then run Phases 3-5 on the merged database.

- **Council delegation**: Phase 3 Council must use real subagent delegation:
  ```
  task(category="deep", run_in_background=true, prompt="Evaluate pair insight_NNN vs insight_MMM as <Persona>: ...")
  ```
  Collect all 5 results via `background_output()`, then aggregate votes. Do NOT simulate Council votes inline.

- **Visual implementation**: All visuals use matplotlib via Python scripts. See `references/diagramming-guide.md` for reusable templates. The agent may adapt templates to document count and complexity but must produce valid PNG files in `research-output/visuals/`.

- **Output path convention**: All investigation output goes to `research-output/` relative to the working directory. For project-specific investigations, use `<project>/research-output/`. Never write outside `research-output/` or `<project>/research-output/`.
