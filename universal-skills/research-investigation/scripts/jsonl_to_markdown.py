#!/usr/bin/env python3
"""
Convert research-investigation JSONL insight database to structured Markdown report.

Usage:
    uv run python scripts/jsonl_to_markdown.py --input <jsonl_file> --output <markdown_file> [--synthesis-file <md>]

Output:
    Structured Markdown report with sections for Scan, Deep-Read, Cross-Connect, Synthesis, and Visuals.

Example:
    uv run python scripts/jsonl_to_markdown.py --input insights.jsonl --output report.md
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def group_by_phase(entries):
    """Group JSONL entries by phase field."""
    groups = {"scan": [], "deep-read": [], "cross-connect": [], "unknown": []}
    for entry in entries:
        phase = entry.get("phase", "unknown")
        if phase in groups:
            groups[phase].append(entry)
        else:
            groups["unknown"].append(entry)
    return groups


def generate_scan_section(scan_entries):
    """Generate Phase 1 SCAN summary tables."""
    if not scan_entries:
        return "## Phase 1: Document Scan Summary\n\n*No scan entries found.*\n\n"

    # Aggregate by document
    docs = {}
    for e in scan_entries:
        doc = e.get("doc", "unknown")
        if doc not in docs:
            docs[doc] = {"pages": 0, "high": 0, "medium": 0, "low": 0}
        docs[doc]["pages"] += 1
        signal = e.get("signal", "low")
        if signal in docs[doc]:
            docs[doc][signal] += 1

    lines = ["## Phase 1: Document Scan Summary\n"]
    lines.append("### Coverage\n")
    lines.append("| Document | Pages Scanned | High Signal | Medium Signal | Low Signal |")
    lines.append("|----------|:------------:|:-----------:|:------------:|:---------:|")
    for doc, stats in sorted(docs.items()):
        lines.append(f"| {doc} | {stats['pages']} | {stats['high']} | {stats['medium']} | {stats['low']} |")
    lines.append("")

    # High-signal pages table
    high_entries = [e for e in scan_entries if e.get("signal") == "high"]
    if high_entries:
        lines.append("### High-Signal Pages\n")
        lines.append("| Document | Page | Section | Summary |")
        lines.append("|----------|:----:|---------|---------|")
        for e in sorted(high_entries, key=lambda x: (x.get("doc",""), x.get("page",0))):
            doc = e.get("doc", "?")
            page = e.get("page", "?")
            section = e.get("section", "?")
            summary = (e.get("summary", "") or "")[:100]
            lines.append(f"| {doc} | {page} | {section} | {summary} |")
        lines.append("")

    return "\n".join(lines)


def generate_deep_read_section(dr_entries):
    """Generate Phase 2 DEEP-READ insight tables and details."""
    if not dr_entries:
        return "## Phase 2: Extracted Insights\n\n*No insights extracted.*\n\n"

    sorted_entries = sorted(dr_entries, key=lambda e: e.get("confidence", 0), reverse=True)

    lines = ["## Phase 2: Extracted Insights\n"]
    lines.append("### Insight Summary\n")
    lines.append("| ID | Document | Page | Key Claim | Evidence | Confidence |")
    lines.append("|----|----------|:----:|-----------|----------|:----------:|")
    for e in sorted_entries:
        eid = e.get("id", "?")
        doc = e.get("doc", "?")
        page = e.get("page", "?")
        claim = (e.get("key_claim", "") or "")[:80]
        ev = e.get("evidence_type", "?")
        conf = e.get("confidence", 0)
        lines.append(f"| {eid} | {doc} | {page} | {claim} | {ev} | {conf:.2f} |")
    lines.append("")

    lines.append("### Insight Details\n")
    for e in sorted_entries:
        eid = e.get("id", "?")
        lines.append(f"#### {eid}\n")
        lines.append(f"**Key Claim:** {e.get('key_claim', '?')}\n")
        lines.append(f"**Evidence:** {e.get('evidence_type', '?')} — {e.get('evidence_detail', '?')}\n")
        lines.append(f"**Strength:** {e.get('strength', '?')} — {e.get('strength_justification', '?')}\n")

        qs = e.get("quality_scores", {})
        qs_str = " | ".join(f"{k}: {v}" for k, v in qs.items())
        lines.append(f"**Quality Scores:** {qs_str}\n")
        lines.append(f"**Confidence:** {e.get('confidence', '?')}\n")

        rels = e.get("builds_on", [])
        cons = e.get("contradicts", [])
        exts = e.get("extends", [])
        pars = e.get("parallels", [])
        lines.append(f"**Relationships:** Builds on: {rels or '[none]'} | Contradicts: {cons or '[none]'} | Extends: {exts or '[none]'} | Parallels: {pars or '[none]'}\n")
        lines.append(f"**Gaps:** {e.get('gaps', '?')}\n")
        lines.append("")

    return "\n".join(lines)


def generate_cross_connect_section(cc_entries):
    """Generate Phase 3 CROSS-CONNECT tables and details."""
    if not cc_entries:
        return "## Phase 3: Cross-Connections\n\n*No connections found.*\n\n"

    lines = ["## Phase 3: Cross-Connections\n"]
    lines.append("### Connection Summary\n")
    lines.append("| ID | Type | Insight A | Insight B | Formula Score | Council Verdict |")
    lines.append("|----|------|-----------|-----------|:------------:|:---------------:|")
    for e in cc_entries:
        eid = e.get("id", "?")
        ctype = e.get("type", "?")
        ia = e.get("insight_a", "?")
        ib = e.get("insight_b", "?")
        fs = e.get("formula_score", 0)
        verdict = e.get("council_verdict", "?")
        lines.append(f"| {eid} | {ctype} | {ia} | {ib} | {fs:.2f} | {verdict} |")
    lines.append("")

    lines.append("### Connection Details\n")
    for e in cc_entries:
        eid = e.get("id", "?")
        ctype = e.get("type", "?")
        lines.append(f"#### {eid} — {ctype}\n")
        lines.append(f"**Insight A:** [{e.get('insight_a','?')}] {_short_claim(e.get('insight_a','?'), cc_entries)}\n")
        lines.append(f"**Insight B:** [{e.get('insight_b','?')}] {_short_claim(e.get('insight_b','?'), cc_entries)}\n")
        lines.append(f"**Mechanism:** {e.get('mechanism', '?')}\n")
        lines.append(f"**Synergy Score:** {e.get('formula_score', '?'):.2f}\n" if isinstance(e.get('formula_score'), (int,float)) else f"**Synergy Score:** {e.get('formula_score','?')}\n")
        cv = e.get("council_votes", {})
        cv_str = " | ".join(f"{k}: {v}" for k, v in cv.items())
        lines.append(f"**Council Votes:** {cv_str}\n")
        verdict = e.get("council_verdict", "?")
        icon = "✅" if verdict == "confirmed" else "⚠️" if verdict == "disputed" else "❌"
        lines.append(f"**Verdict:** {icon} {verdict}\n")
        lines.append("")

    return "\n".join(lines)


def _short_claim(insight_id, cc_entries):
    """Placeholder for insight claim lookup. Returns insight ID as fallback."""
    return insight_id


def generate_visuals_section():
    """Generate Phase 5 visuals listing."""
    lines = ["## Generated Visuals\n"]
    lines.append("| File | Description |")
    lines.append("|------|-------------|")
    lines.append("| visuals/coverage-heatmap.png | Document coverage heatmap (Phase 1→2 gate) |")
    lines.append("| visuals/insight-scatter.png | Insight quality scatterplot (Phase 2→3 gate) |")
    lines.append("| visuals/connection-graph.png | Insight connection graph (Phase 3→4 gate) |")
    lines.append("| visuals/synthesis-dashboard.png | Synthesis dashboard (Phase 4→5 gate) |")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Convert research-investigation JSONL to structured Markdown report"
    )
    parser.add_argument("--input", required=True, type=Path, help="Input JSONL file")
    parser.add_argument("--output", required=True, type=Path, help="Output Markdown file")
    parser.add_argument("--synthesis-file", type=Path, help="Synthesis markdown to embed in report")
    args = parser.parse_args()

    input_path = args.input.resolve()
    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    # Parse JSONL
    entries = []
    with open(input_path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    print(f"Parsed {len(entries)} entries from {input_path.name}", file=sys.stderr)

    # Extract metadata
    docs = list({e.get("doc", "unknown") for e in entries if "doc" in e})
    insights = [e for e in entries if e.get("phase") == "deep-read"]

    # Group by phase
    groups = group_by_phase(entries)

    # Build report
    timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
    report = []
    report.append("# Research Investigation Report\n")
    report.append(f"**Generated:** {timestamp}\n")
    report.append(f"**Documents:** {', '.join(sorted(docs)) if docs else 'none'}\n")
    report.append(f"**Total Insights:** {len(insights)}\n")
    report.append("\n---\n")

    report.append(generate_scan_section(groups["scan"]))
    report.append("---\n")
    report.append(generate_deep_read_section(groups["deep-read"]))
    report.append("---\n")
    report.append(generate_cross_connect_section(groups["cross-connect"]))

    # Embed synthesis if provided
    if args.synthesis_file and args.synthesis_file.exists():
        report.append("---\n")
        report.append("## Phase 4: Synthesis\n")
        syn_content = args.synthesis_file.read_text(encoding="utf-8", errors="replace")
        # Extract just the synthesis sections
        for heading in ["Points of Convergence", "Core Tension", "The Blind Spot", "Recommended Actions"]:
            idx = syn_content.find(f"## {heading}")
            if idx != -1:
                end = len(syn_content)
                next_idx = min([syn_content.find(f"## {h}", idx+1) for h in ["Points of Convergence", "Core Tension", "The Blind Spot", "Recommended Actions"] if syn_content.find(f"## {h}", idx+1) != -1] or [end])
                report.append(syn_content[idx:next_idx].strip() + "\n")

    report.append("---\n")
    report.append(generate_visuals_section())

    content = "\n".join(report)
    args.output.write_text(content, encoding="utf-8")
    print(f"Report written to {args.output} ({len(content):,} chars)", file=sys.stderr)


if __name__ == "__main__":
    main()
