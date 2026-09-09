#!/usr/bin/env python3
"""
Validate phase gate conditions for research-investigation pipeline.

Usage:
    uv run python scripts/verify_gates.py --phase <phase> --input <path> [--output <file>] [options]

Output:
    JSON object with phase, passed (bool), checks (list), violations (list)

Example:
    uv run python scripts/verify_gates.py --phase=scan --input insights.jsonl --doc-pages paper-a.md:25 --doc-pages paper-b.md:12
    uv run python scripts/verify_gates.py --phase=deep-read --input insights.jsonl
    uv run python scripts/verify_gates.py --phase=synthesize --synthesis-file report.md
"""

import argparse
import json
import sys
from pathlib import Path


def check_find(research_dir):
    """Phase 0: FIND gate. Checks research-output directory has >=1 doc + README."""
    checks = []
    rd = research_dir.resolve()
    rd_exists = rd.is_dir()
    checks.append({"name": "research_dir_exists", "passed": rd_exists,
                   "detail": f"Directory {'exists' if rd_exists else 'missing'}: {rd}"})
    if not rd_exists:
        return checks, ["Research output directory does not exist"]

    md_files = list(rd.glob("*.md"))
    has_docs = len(md_files) >= 1
    checks.append({"name": "has_documents", "passed": has_docs,
                   "detail": f"Found {len(md_files)} markdown file(s)"})

    readme = (rd / "README.md").exists()
    checks.append({"name": "has_readme", "passed": readme,
                   "detail": "README.md exists" if readme else "README.md missing"})

    violations = []
    if not has_docs:
        violations.append("No markdown documents found in research-output/")
    if not readme:
        violations.append("README.md not found in research-output/")
    return checks, violations


def check_scan(jsonl_lines, doc_pages):
    """Phase 1: SCAN gate. >=80% page coverage across all docs."""
    checks = []
    scan_entries = [json.loads(line) for line in jsonl_lines if json.loads(line).get("phase") == "scan"]
    total_scanned = len(scan_entries)

    docs_found = {e.get("doc", "unknown") for e in scan_entries}
    total_pages = sum(doc_pages.values())
    total_pages = max(total_pages, total_scanned)  # Avoid division by zero

    coverage = total_scanned / total_pages if total_pages > 0 else 0
    passes = coverage >= 0.8
    checks.append({"name": "coverage", "passed": passes,
                   "detail": f"{total_scanned}/{total_pages} pages ({coverage:.1%}) — threshold: 80%"})

    missing = [d for d, n in doc_pages.items() if d not in docs_found]
    all_docs = len(missing) == 0
    checks.append({"name": "all_docs_scanned", "passed": all_docs,
                   "detail": f"Docs: {sorted(docs_found)}" if all_docs else f"Missing: {missing}"})

    violations = []
    if not passes:
        violations.append(f"Coverage {coverage:.1%} below 80% threshold")
    if missing:
        violations.append(f"No scan entries for documents: {missing}")
    return checks, violations


def check_deep_read(jsonl_lines, min_insights=5, min_confidence=0.3):
    """Phase 2: DEEP-READ gate. >=N insights, all fields, confidence >=min."""
    checks = []
    dr_entries = [json.loads(line) for line in jsonl_lines if json.loads(line).get("phase") == "deep-read"]
    count = len(dr_entries)
    passes_count = count >= min_insights
    checks.append({"name": "insight_count", "passed": passes_count,
                   "detail": f"{count} insights — threshold: {min_insights}"})

    required = ["key_claim", "evidence_type", "strength", "confidence"]
    incomplete = []
    low_conf = []
    for e in dr_entries:
        missing_fields = [f for f in required if f not in e or not e[f]]
        if missing_fields:
            incomplete.append({"id": e.get("id", "unknown"), "missing": missing_fields})
        if e.get("confidence", 0) < min_confidence:
            low_conf.append({"id": e.get("id", "unknown"), "confidence": e.get("confidence")})

    all_complete = len(incomplete) == 0
    checks.append({"name": "all_fields_complete", "passed": all_complete,
                   "detail": "All insights complete" if all_complete else f"Incomplete: {len(incomplete)}"})

    all_conf = len(low_conf) == 0
    checks.append({"name": "confidence_minimum", "passed": all_conf,
                   "detail": f"All confidence >= {min_confidence:.1f}" if all_conf else f"Low confidence: {len(low_conf)}"})

    violations = []
    if not passes_count:
        violations.append(f"Only {count} insights — need at least {min_insights}")
    if incomplete:
        violations.append(f"{len(incomplete)} insights missing required fields")
    if low_conf:
        violations.append(f"{len(low_conf)} insights below confidence {min_confidence}")
    return checks, violations


def check_cross_connect(jsonl_lines):
    """Phase 3: CROSS-CONNECT gate. >=3 types, >=1 compounds, >=1 contradicts."""
    checks = []
    cc_entries = [json.loads(line) for line in jsonl_lines if json.loads(line).get("phase") == "cross-connect"]
    types = {e.get("type", "") for e in cc_entries}
    type_count = len(types)
    passes_types = type_count >= 3
    checks.append({"name": "connection_types", "passed": passes_types,
                   "detail": f"{type_count} types found: {types} — threshold: 3"})

    has_compounds = any(e.get("type") == "compounds" for e in cc_entries)
    checks.append({"name": "has_synergy", "passed": has_compounds,
                   "detail": "Compounds connection found" if has_compounds else "No compounds (synergy) connection"})

    has_conflicts = any(e.get("type") == "contradicts" for e in cc_entries)
    checks.append({"name": "has_conflict", "passed": has_conflicts,
                   "detail": "Contradiction found" if has_conflicts else "No conflicts — Council must confirm"})

    violations = []
    if not passes_types:
        violations.append(f"Only {type_count} connection types — need at least 3 (found: {types})")
    if not has_compounds:
        violations.append("No 'compounds' (synergy) connection found")
    if not has_conflicts:
        violations.append("No 'contradicts' connection — verify with Council")
    return checks, violations


def check_synthesize(synthesis_file):
    """Phase 4: SYNTHESIZE gate. All 4 sections with >=2 lines content."""
    checks = []
    if not synthesis_file.exists():
        return [{"name": "file_exists", "passed": False, "detail": f"File not found: {synthesis_file}"}], ["Synthesis file not found"]

    content = synthesis_file.read_text(encoding="utf-8")
    sections = {
        "Points of Convergence": "## Points of Convergence",
        "Core Tension": "## Core Tension",
        "Blind Spot": "## The Blind Spot",
        "Recommended Actions": "## Recommended Actions"
    }

    violations = []
    for name, heading in sections.items():
        idx = content.find(heading)
        if idx == -1:
            checks.append({"name": f"section_{name.lower().replace(' ','_')}", "passed": False,
                           "detail": f"Missing section: {heading}"})
            violations.append(f"Missing section: {heading}")
        else:
            lines = content[idx:].split("\n")
            body_lines = [l for l in lines[1:] if l.strip() and not l.strip().startswith("#")]
            has_content = len(body_lines) >= 2
            checks.append({"name": f"section_{name.lower().replace(' ','_')}", "passed": has_content,
                           "detail": f"Found with {len(body_lines)} body lines"})

    actions_idx = content.find("## Recommended Actions")
    action_count = 0
    if actions_idx != -1:
        action_section = content[actions_idx:]
        action_count = action_section.count("|") // 10  # Rough estimate of table rows
    has_actions = action_count >= 3
    checks.append({"name": "action_count", "passed": has_actions,
                   "detail": f"~{action_count} actions — threshold: 3"})
    if not has_actions:
        violations.append("Less than 3 recommended actions found")

    return checks, violations


def check_report(research_dir):
    """Phase 5: REPORT gate. All output files present."""
    checks = []
    rd = research_dir.resolve()
    files_required = ["report.md", "insights.jsonl", "README.md"]
    violations = []

    for fname in files_required:
        fpath = rd / fname
        exists = fpath.exists()
        checks.append({"name": f"file_{fname}", "passed": exists,
                       "detail": f"{fname} {'exists' if exists else 'missing'}"})
        if not exists:
            violations.append(f"Missing: {fname}")

    visuals_dir = rd / "visuals"
    if visuals_dir.is_dir():
        images = list(visuals_dir.glob("*.png")) + list(visuals_dir.glob("*.svg"))
        has_visuals = len(images) >= 4
        checks.append({"name": "visuals", "passed": has_visuals,
                       "detail": f"{len(images)} visual files found — threshold: 4"})
        if not has_visuals:
            violations.append(f"Only {len(images)} visuals — need 4")
    else:
        checks.append({"name": "visuals", "passed": False, "detail": "visuals/ directory missing"})
        violations.append("visuals/ directory missing")

    return checks, violations


def main():
    parser = argparse.ArgumentParser(
        description="Validate phase gate conditions for research-investigation pipeline"
    )
    parser.add_argument("--phase", required=True, choices=["find","scan","deep-read","cross-connect","synthesize","report"],
                        help="Phase to validate")
    parser.add_argument("--input", type=Path, help="Input path (JSONL file or research-output directory)")
    parser.add_argument("--output", type=Path, help="Output file (defaults to stdout)")
    parser.add_argument("--doc-pages", nargs="*", default=[],
                        help="Document page counts as docname:N (e.g. paper-a.md:25)")
    parser.add_argument("--min-insights", type=int, default=5, help="Minimum insight count (default: 5)")
    parser.add_argument("--min-confidence", type=float, default=0.3, help="Minimum confidence (default: 0.3)")
    parser.add_argument("--synthesis-file", type=Path, help="Synthesis markdown file (for synthesize phase)")
    parser.add_argument("--no-conflicts", action="store_true", help="Verify no-conflicts is confirmed")
    args = parser.parse_args()

    if not args.input and args.phase not in ("synthesize",):
        print("Error: --input required for phase", args.phase, file=sys.stderr)
        sys.exit(1)

    if args.phase == "find":
        checks, violations = check_find(args.input)
    elif args.phase == "scan":
        lines = args.input.read_text(encoding="utf-8").strip().split("\n") if args.input.exists() else []
        doc_pages = {}
        for dp in args.doc_pages:
            if ":" in dp:
                doc, n = dp.rsplit(":", 1)
                doc_pages[doc] = int(n)
        checks, violations = check_scan(lines, doc_pages)
    elif args.phase == "deep-read":
        lines = args.input.read_text(encoding="utf-8").strip().split("\n") if args.input.exists() else []
        checks, violations = check_deep_read(lines, args.min_insights, args.min_confidence)
    elif args.phase == "cross-connect":
        lines = args.input.read_text(encoding="utf-8").strip().split("\n") if args.input.exists() else []
        checks, violations = check_cross_connect(lines)
    elif args.phase == "synthesize":
        if not args.synthesis_file:
            print("Error: --synthesis-file required for synthesize phase", file=sys.stderr)
            sys.exit(1)
        checks, violations = check_synthesize(args.synthesis_file)
    elif args.phase == "report":
        checks, violations = check_report(args.input)

    passed = len(violations) == 0
    result = {"phase": args.phase, "passed": passed, "checks": checks, "violations": violations}
    output = json.dumps(result, indent=2)

    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(f"Output written to {args.output}")
    else:
        print(output)

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
