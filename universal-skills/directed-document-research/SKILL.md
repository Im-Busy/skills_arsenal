---
name: directed-document-research
description: Search the web for PDFs and documents from authoritative sources on a given topic, batch download, convert to markdown for review, filter by relevance to the current task, keep only useful files in a project-relative research directory, delete the rest, and report findings. Use when the user asks to research a topic by finding and reviewing documents from trusted sources — academic papers, professional body publications, government reports, industry standards, white papers — for any domain.
allowed-tools: Read Write Edit Bash(tavily_tavily-search:*, ttavily_tavily-extract:*, ttavily_tavily-crawl:*, exa_web_search_exa:*, exa_web_fetch_exa:*, webfetch:*)
license: MIT license
metadata:
    skill-author: Kilo from joeychiu/reading-CFS-IS-BS
---

# Directed Document Research

## Overview

Find, download, convert, filter, and organize documents from trusted web sources on any topic. This skill guides the agent through a 5-phase pipeline: search → download → convert → filter → report. The output is a curated set of documents saved in a project-relative directory, with all noise removed.

**Key principle:** search broadly, download generously, but keep ruthlessly. Only documents that are directly usable for the current task survive the filter.

## When to Use This Skill

This skill should be used when the user asks to:
- "Research {topic}" with an implied document-gathering component
- "Find PDFs/papers/reports about {topic} from {trusted sources}"
- "Search for what {profession/industry} does regarding {practice/methodology}"
- "Get me the best resources on {topic}"
- Any request that combines web search + document review + curation

Do NOT use this skill for:
- Finding code examples or API documentation (use Context7 or direct code search)
- Searching for specific known documents by title (just use tavily-search or exa)
- Reading a single known URL (use webfetch directly)
- General Q&A that doesn't require document review

## Workflow

### Phase 1 — Search (Broad)

Search for PDFs from authoritative sources. Use multiple queries at different angles to maximize coverage.

**Source credibility tiers (prefer higher tiers):**

| Tier | Source Type | Examples |
|------|-------------|----------|
| 1 | Professional bodies, standards organizations | CFA Institute, IEEE, ISO, NIST, AICPA, ACCA |
| 2 | Government agencies, regulators | SEC, Federal Reserve, BIS, IMF, government .gov sites |
| 3 | Major consulting firms, Big 4 | McKinsey, Deloitte, PwC, EY, KPMG, BCG, Bain |
| 4 | Established academic journals, university presses | Nature, arXiv (recent, highly cited), university .edu |
| 5 | Industry associations, reputable foundations | Brookings, RAND, trade associations |

**Search strategy:**
- Use `tavily-search` with `search_depth: "advanced"` and `max_results: 15`
- Run 2-3 searches in parallel with different query angles
- Append `filetype:pdf` to every query
- Use `exa_web_search_exa` for academic-focused searches
- Target queries like: `{professional_body} "{topic}" methodology guide filetype:pdf`

**Example queries for a topic like "financial statement analysis":**
```
CFA "financial statement analysis" framework filetype:pdf
Deloitte PwC "financial statement analysis" methodology filetype:pdf
"financial statement analysis" ratios red flags best practices filetype:pdf
```

### Phase 2 — Download (Batch)

Create a staging directory for research downloads. Download all candidate PDFs.

**Directory convention:**
- Create `<project>/data/research/` (or `<project>/docs/research/`) if it doesn't exist
- All downloads and conversions go here
- Use a temp script for batch downloading to avoid repetitive tool calls

**Download script template (`_download.py`, self-deleting after use):**
```python
import requests
from pathlib import Path

OUT_DIR = Path("data/research")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = [
    ("<url1>", "<descriptive-filename1>.pdf"),
    ("<url2>", "<descriptive-filename2>.pdf"),
]

for url, filename in SOURCES:
    path = OUT_DIR / filename
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    path.write_bytes(resp.content)
    print(f"Downloaded {filename}: {path.stat().st_size:,} bytes")
```

Run once, then delete the script.

**Troubleshooting:** if a URL fails with an anti-bot block, try `webfetch` directly. If that also fails, skip the source – it's better to move on than to spend time on one recalcitrant URL.

### Phase 3 — Convert (PDF → Markdown)

Convert every downloaded PDF to markdown for review. Use the most available converter.

**Priority order for conversion tools:**
1. **PyMuPDF (fitz)** — if available in project dependencies, use this. Fast, works offline.
2. **marker** — if `marker` CLI is in path. Produces richer output including tables.
3. **pandoc** — fallback. `pandoc input.pdf -t markdown -o output.md`
4. **webfetch** — if the PDF URL hasn't been deleted yet, try fetching as markdown.

**Conversion script template (`_convert.py`, self-deleting after use):**
```python
import fitz
from pathlib import Path

RESEARCH_DIR = Path("data/research")

for pdf_path in RESEARCH_DIR.glob("*.pdf"):
    md_path = pdf_path.with_suffix(".md")
    doc = fitz.open(pdf_path)
    text = "".join(page.get_text() for page in doc)
    doc.close()
    if not text.strip():
        print(f"SKIP {pdf_path.name}: no extractable text")
        continue
    md_path.write_text(text, encoding="utf-8")
    print(f"Converted {pdf_path.name} -> {md_path.name} ({len(text):,} chars)")
```

After conversion, delete the script.

### Phase 4 — Filter (Ruthless)

This is the critical phase. Read each markdown file and decide: keep or delete.

**Relevance test (all must pass to KEEP):**

1. **Source check** — is it from a credible source (Tier 1-5)? Skip blog posts, student papers (unless PhD thesis), marketing material.
2. **Content check** — does it address the specific topic/question, or just mention it tangentially?
3. **Usability check** — would this document's methods, frameworks, or data be directly usable in our work?
4. **Density check** — is it substantive (data, frameworks, methodology), or just introductory fluff?

**Red flags for deletion:**
- Undergraduate/bachelor's student projects or reports
- Blog posts, social media threads, marketing PDFs
- Documents that are about the right topic but for an entirely different context (e.g., personal finance when doing corporate analysis)
- PDFs where the extractable text is corrupt or < 500 chars
- Documents where the author/source is unknown/unverifiable
- Meta-documents (audit guides about how to audit, not how to analyze)

**Process:**
1. Read each markdown file (first 100-150 lines is usually enough to judge)
2. Apply the relevance test
3. For documents that FAIL: delete BOTH the PDF and the markdown
4. For documents that PASS: keep both

### Phase 5 — Report

Create a `README.md` in the research directory summarizing:

```markdown
# Research References

<brief 1-2 line context about what was researched>

## Kept

### <document-name>
**Source:** <institution/author> (<date>)
**Why relevant:** <1-2 sentences on direct applicability>
```

Also report to the user:
- How many documents were downloaded
- How many were kept and deleted
- Where the research directory is (relative path)
- A 1-line summary of each kept document

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Read every PDF to the end before deciding | Read first 100-150 lines of markdown — the introduction, abstract, and table of contents are usually decisive |
| Keep borderline documents "just in case" | Delete them. It's better to have 3 excellent sources than 10 mediocre ones |
| Spend >2 minutes trying to download one URL | Skip it. Timebox each download to 60 seconds |
| Use the staging directory for anything else | Keep it pristine. One research session = one clean batch |
| Leave download/conversion scripts behind | Delete helper scripts immediately after use |
| Keep PDFs without converting them | Always convert to markdown for review. The agent can't read PDFs natively |
| Search only one angle | Always 2-3 different query formulations in parallel |

## Example Session

**User:** "Find me PDFs from CFA Institute and Big4 firms on financial statement analysis methodology."

**Agent flow:**
1. Searches `CFA "financial statement analysis" methodology filetype:pdf` and `Deloitte PwC "financial statement analysis" ratios filetype:pdf` in parallel
2. Downloads 3 PDFs: CFA equity research essentials, a student Big4 comparison, a fraud detection paper
3. Converts all 3 to markdown via PyMuPDF
4. Reads each: keeps CFA document (industry standard, directly applicable) and fraud detection paper (red flag frameworks). Deletes student project (undergraduate paper, not methodology)
5. Reports: "3 downloaded → 2 kept, 1 deleted. CFA report structure and fraud detection framework saved to `data/research/`."
