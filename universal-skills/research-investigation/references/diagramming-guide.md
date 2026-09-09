# Diagramming Guide — Mandatory Visual Outputs

Diagrams are **MANDATORY**, not optional. Every phase transition in the research-investigation workflow **must** produce exactly one visual artifact. The agent **proceeds to the next phase only after the visual file exists** at its canonical path.

## Why Diagrams Are Non-Negotiable

The act of diagramming forces structural thinking. Text lets you hand-wave — diagrams do not. When you must place every document on a heatmap grid, every insight on a scatterplot, or every connection on a graph, you will often discover:

- **Gaps** — pages you skimmed, not read
- **Weak insights** — claims that feel important but have no evidence
- **Missed connections** — two insights from different documents that say the same thing in different words
- **Overclaiming** — a "strong" insight that doesn't survive labeling on a confidence axis

**Rule of thumb**: If you cannot diagram it, you do not understand it well enough to proceed.

---

## Visual 1: Coverage Heatmap (Phase 1→2 gate)

### Purpose
Shows **WHERE** valuable content is — prevents the agent from skipping pages or claiming coverage without reading.

### What to Show
- **Rows** = documents being researched
- **Columns** = page ranges (e.g., pp.1-5, 6-10, 11-15, 16-20, 21-25)
- **Cells** = signal density, color-coded:
  - 🟢 **Green** = high signal (key findings, data, unique claims)
  - 🟡 **Yellow** = medium signal (supporting context, useful examples)
  - 🔴 **Red** = low signal (boilerplate, tangents, filler)
  - ⬜ **Gray** = not yet scanned (must be resolved before proceeding)

### Tool Recommendations
- **Mermaid** (simpler, faster) — use `block-beta` with 6-column layout
- **cli-anything-drawio** (richer, custom styling) — for heatmaps with many documents

### Mermaid Template

```mermaid
---
config:
  layout: elk
---
block-beta
  columns 6
  docA["doc-a.md"]:1
  docA_p1_5["pp.1-5\n🟢":1] docA_p6_10["pp.6-10\n🟡":1] docA_p11_15["pp.11-15\n🔴":1] docA_p16_20["pp.16-20\n🟢":1] docA_p21_25["pp.21-25\n🔴":1]
  docB["doc-b.md"]:1
  docB_p1_5["pp.1-5\n🟡":1] docB_p6_10["pp.6-10\n🟢":1] docB_p11_15["pp.11-15\n🟢":1] docB_p16_20["pp.16-20\n🟡":1] docB_p21_25["pp.21-25\n🔴":1]
```

### Gate Check
- File exists at `research-output/visuals/coverage-heatmap.png`
- Every document row has at least one non-gray cell
- No all-green rows (indicates dishonest scanning)

### Anti-Patterns
- **Flat heatmap**: All cells the same color → indicates the agent did not actually scan each page range. Genuine documents have variance. If every cell is green, you skimmed.
- **Missing rows**: Documents you read but did not include on the heatmap → you skipped the visual step.
- **Skip-and-dump**: Claiming "coverage verified" without generating the file → gate enforcement catches this.

---

## Visual 2: Insight Scatterplot (Phase 2→3 gate)

### Purpose
Shows **WHICH** insights are strong and novel — a visual quality calibration that prevents weak or known insights from polluting the synthesis.

### What to Show
- **X-axis** = novelty score (0–10): How surprising/unexpected is this insight?
- **Y-axis** = confidence score (0–10): How well-supported by evidence?
- **Each point** = an insight, sized by explanatory_power (how much of the topic does it explain?)
- **Labels** = every point must be labeled with its insight ID

### Quadrant Interpretation

| Quadrant | Label | Action |
|----------|-------|--------|
| Top-right (high novelty × high confidence) | **Solid & Novel** | **Keep** — these are your primary findings |
| Top-left (low novelty × high confidence) | **Solid but Known** | **Reference** — cite as prior art, do not claim as discovery |
| Bottom-right (high novelty × low confidence) | **Speculative & Novel** | **Verify** — flag for deeper investigation |
| Bottom-left (low novelty × low confidence) | **Weak & Known** | **Discard** — not worth reporting |

### Tool Recommendations
- **cli-anything-mermaid** (scatterplot) — adequate for <30 insights
- **cli-anything-drawio** (custom coordinate grid) — better for large sets

### Gate Check
- File exists at `research-output/visuals/insight-scatter.png`
- Every insight from the extraction phase appears as exactly one point
- Every point has a legible label

### Requirements
- **Label every point** with its insight ID (e.g., `I-01`, `I-12`). An unlabeled scatterplot is decoration, not analysis.
- Size encoding must be visually discriminable (min 8px, max 40px diameter).
- Draw quadrant dividing lines (dashed, at x=5 and y=5).

---

## Visual 3: Connection Graph (Phase 3→4 gate)

### Purpose
Shows **HOW** insights relate to each other — this is the single most important visual in the workflow. The connection graph is where raw insights become structured knowledge.

### What to Show
- **Nodes** = insights, sized by confidence score
- **Edges** = connections between insights, color-coded by relationship type:
  - 🟢 **Green** — compounds (using both together is stronger than either alone)
  - 🔵 **Blue** — builds-on (one insight provides foundation for another)
  - 🔴 **Red** — contradicts (insights conflict; must be resolved in synthesis)
  - ⬜ **Gray** — parallels (different language, same underlying idea)
  - 🟠 **Orange** — extends (one insight generalizes or limits another)
- **Edge thickness** = council score (how many sources/votes support the connection)

### Tool Recommendations
- **cli-anything-drawio** (best for complex graphs with many edges and styling)
- **Mermaid flowchart** (adequate for ≤15 nodes with simple edge types)

### Layout Guidance
- **Force-directed** layout for organic discovery graphs (shows clusters naturally)
- **Hierarchical** layout for causal chains (A → B → C → D structure)
- Do **not** use circular layout — it obscures structural importance

### Gate Check
- File exists at `research-output/visuals/connection-graph.png`
- Every insight from the scatterplot appears as a node
- **Must include a legend** for edge colors (otherwise the reader cannot interpret it)

### Requirements
- Legend must be embedded in the diagram or adjacent on the same canvas
- Edges without a label default to "parallels" (gray) — but if you cannot name the relationship, question whether the connection is real
- Isolated nodes (no edges) are valid — the graph honestly shows "no connections found"

---

## Visual 4: Synthesis Dashboard (Phase 4→5 gate)

### Purpose
The artifact the **user actually looks at**. Everything prior was internal analysis. This is your single-page deliverable.

### What to Show — Three Panels

#### Panel 1: Miniature Connection Graph
- Scaled-down version of the connection graph from Visual 3
- Legend included (may be smaller, but must be readable)
- Highlights the top 3 most-connected insights (e.g., bold outline or glow effect)

#### Panel 2: Decision Matrix
- **2×2 grid**: Feasibility (easy → hard) × Impact (low → high)
- Each **Recommended Action** plotted as a labeled point
- Quadrants:
  - **High impact, easy** → Quick wins (do immediately)
  - **High impact, hard** → Strategic bets (plan for)
  - **Low impact, easy** → Low-hanging fruit (do if time allows)
  - **Low impact, hard** → Avoid (skip)

#### Panel 3: Callout Boxes (3 mandatory)
1. **Convergence Summary** — Where do most insights agree? What is the confident takeaway?
2. **Core Tension** — What is the single hardest conflict or unresolved question?
3. **Blind Spot** — What is notably absent from the research? What should exist but does not?

### Tool
**cli-anything-drawio** (required — this is a composite visual with three distinct panels on one canvas)

### Gate Check
- File exists at `research-output/visuals/synthesis-dashboard.png`
- All three panels are present and readable
- The miniature graph matches the topology of Visual 3 (no fabricating connections)
- Callout boxes have actual content (not placeholder text)

### This Is THE Deliverable
Make it readable. Use a clean layout with clear panel boundaries. Font size should be legible at a standard screen. If printed, it should make sense in grayscale (check your color choices).

---

## Gate Enforcement

```
verify_gates.py --phase=<phase> checks that the visual file exists.
If the file doesn't exist → FAIL → agent must generate it before proceeding.
```

### Gate Mapping

| Phase Transition | Visual | Gate Command | File Path |
|-----------------|--------|-------------|-----------|
| Phase 1 → 2 | Coverage Heatmap | `verify_gates.py --phase=1` | `research-output/visuals/coverage-heatmap.png` |
| Phase 2 → 3 | Insight Scatterplot | `verify_gates.py --phase=2` | `research-output/visuals/insight-scatter.png` |
| Phase 3 → 4 | Connection Graph | `verify_gates.py --phase=3` | `research-output/visuals/connection-graph.png` |
| Phase 4 → 5 | Synthesis Dashboard | `verify_gates.py --phase=4` | `research-output/visuals/synthesis-dashboard.png` |

**No visual → no phase advance.** This is enforced programmatically. The agent cannot skip, postpone, or "come back to" a visual. Generate it at the gate or do not pass through.

---

## Minimum Viable Visuals

The requirement is that the visual **EXISTS** and is **HONEST** — not that it is complex.

### Scaling Rules

| Research Scope | Visual 1 | Visual 2 | Visual 3 | Visual 4 |
|---------------|----------|----------|----------|----------|
| Tiny (1–2 docs, 5 pages) | 2-row heatmap, 2 columns each | 1–5 point scatterplot | 2–5 node graph | Mini dashboard with 1–2 actions |
| Medium (3–5 docs, 30 pages) | 5-row heatmap, 6 columns each | 5–15 point scatterplot | 5–15 node graph | Full dashboard |
| Large (6+ docs, 100 pages) | Full grid | 15+ point scatterplot | 15+ node graph | Full dashboard with sub-panels |

### What "Valid" Means

- **Coverage Heatmap**: A single page with one document and one cell showing "pp.1-2: 🟢" is valid for a 2-page memo. What matters is that you read every page and rated each one honestly.
- **Insight Scatterplot**: A single point labeled "I-01" at (novelty=7, confidence=8) is valid for a document that yielded one insight. The honesty of the placement is the value.
- **Connection Graph**: Two nodes with a gray edge labeled "parallels" is valid for two insights that say similar things. The graph that honestly shows "only 1 insight found, no connections possible" is **more valuable** than a fabricated graph with fake connections.
- **Synthesis Dashboard**: A dashboard with 1 action in the decision matrix and 3 honest callout boxes (even if "Core Tension: None found — all insights agree") is valid.

### Anti-Patterns for Minimum Viable

- Adding fake rows/columns to a heatmap to make it "look comprehensive"
- Placing an insight at (5, 5) on the scatterplot to avoid committing to a judgment
- Adding meaningless edges to a connection graph to avoid isolated nodes
- Filling callout boxes with fluff ("Further analysis may reveal additional insights")

**Honesty is the metric. An honest simple visual beats a dishonest complex one every time.**

---

## Quick Reference: Tool Selection by Visual

| Visual | Recommended Tool | Fallback |
|--------|-----------------|----------|
| Coverage Heatmap | `cli-anything-mermaid` (block-beta) | `cli-anything-drawio` (table) |
| Insight Scatterplot | `cli-anything-drawio` (grid + circles) | `cli-anything-mermaid` (block) |
| Connection Graph | `cli-anything-drawio` (nodes + edges + legend) | Mermaid flowchart |
| Synthesis Dashboard | `cli-anything-drawio` (composite panels) | None — drawio is required |

Always prefer the recommended tool for each visual. Fallback only when the tool is unavailable.