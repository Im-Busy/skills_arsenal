#!/usr/bin/env python3
"""
Merge JSONL insight databases from multiple research sessions, deduplicating by
insight ID.  Phase-specific strategies are hardcoded per the research pipeline;
the --strategy flag acts as a fallback for unknown phases, and manual mode
emits a conflict report instead of writing output.

Usage:
    merge_sessions.py --inputs file1.jsonl file2.jsonl [file3.jsonl ...]
                      --output merged.jsonl
                      [--strategy newest|highest_confidence|manual]
                      [--dedup-by id]

Output:
    Merged JSONL file + textual summary to stdout.
    With --strategy manual: conflict report JSON to stdout (no output file).

Examples:
    uv run python scripts/merge_sessions.py --inputs s1.jsonl s2.jsonl --output merged.jsonl
    uv run python scripts/merge_sessions.py --inputs s1.jsonl s2.jsonl --output merged.jsonl --strategy highest_confidence
"""

import argparse
import json
import sys
from pathlib import Path

# Phase-specific dedup strategies (these are fixed and override --strategy
# for known phases; --strategy only applies to "unknown" phase entries).
PHASE_STRATEGIES = {
    "scan": "newest",
    "deep-read": "highest_confidence",
    "cross-connect": "newest",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_entries(paths):
    """Read JSONL entries from *paths*, tagging each with source metadata.

    Each entry gets two internal fields:
        _source_idx  – index into *paths* (0-based)
        _source_file – basename of the file it came from
    """
    entries = []
    for idx, path in enumerate(paths):
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                data = json.loads(stripped)
                data["_source_idx"] = idx
                data["_source_file"] = p.name
                entries.append(data)
    return entries


def find_differences(e1, e2, dedup_by):
    """Return dict of fields that differ between *e1* and *e2*.

    Internal keys (``_source_*``) and the dedup key itself are skipped.
    """
    diff = {}
    all_keys = set(e1.keys()) | set(e2.keys())
    skip = {"_source_idx", "_source_file", dedup_by}
    for k in all_keys:
        if k in skip:
            continue
        v1 = e1.get(k)
        v2 = e2.get(k)
        if v1 != v2:
            diff[k] = [v1, v2]
    return diff


def dedup_group(entries, strategy, dedup_by):
    """Deduplicate *entries* on the field *dedup_by* using *strategy*.

    Returns ``(merged_list, conflict_list)``.  Entries without the dedup key
    pass through without deduplication (preserved as-is).
    """
    seen = {}
    conflicts = []
    no_key = []

    for entry in entries:
        key = entry.get(dedup_by)
        if key is None:
            no_key.append(entry)
            continue

        if key in seen:
            if strategy == "manual":
                existing = seen[key]
                conflicts.append({
                    "id": key,
                    "sources": [existing["_source_file"], entry["_source_file"]],
                    "differences": find_differences(existing, entry, dedup_by),
                })
            elif strategy == "newest":
                # Keep entry from the latest input file (higher source index)
                if entry["_source_idx"] >= seen[key]["_source_idx"]:
                    seen[key] = entry
            elif strategy == "highest_confidence":
                if entry.get("confidence", 0) > seen[key].get("confidence", 0):
                    seen[key] = entry
        else:
            seen[key] = entry

    return list(seen.values()) + no_key, conflicts


def count_by_phase(entries):
    """Return ``{phase: count}`` for *entries* (defaults unknown phase)."""
    counts = {}
    for e in entries:
        phase = e.get("phase", "unknown")
        counts[phase] = counts.get(phase, 0) + 1
    return counts


def merge_sessions(paths, strategy, dedup_by):
    """Orchestrate: read, group by phase, dedup per phase, return results.

    Returns ``(merged_entries, stats_dict, conflict_list)``.
    """
    all_entries = read_entries(paths)
    total_pre = len(all_entries)

    # Group entries by their "phase" field
    by_phase = {}
    for e in all_entries:
        phase = e.get("phase", "unknown")
        by_phase.setdefault(phase, []).append(e)

    merged = []
    all_conflicts = []

    for phase, entries in by_phase.items():
        # Resolve strategy for this phase
        phase_strat = PHASE_STRATEGIES.get(phase, strategy)
        if strategy == "manual":       # manual overrides everything
            phase_strat = "manual"

        deduped, conflicts = dedup_group(entries, phase_strat, dedup_by)
        merged.extend(deduped)
        all_conflicts.extend(conflicts)

    # Strip internal tracking fields before returning
    for e in merged:
        e.pop("_source_idx", None)
        e.pop("_source_file", None)

    total_post = len(merged)
    stats = {
        "total_pre": total_pre,
        "total_post": total_post,
        "duplicates_resolved": total_pre - total_post,
        "by_phase": count_by_phase(merged),
    }
    return merged, stats, all_conflicts


def print_summary(stats, num_inputs):
    """Print merge summary table to stdout."""
    phase_str = ", ".join(
        f"{k}: {v}" for k, v in sorted(stats["by_phase"].items())
    )
    print("Merge Summary:")
    print(f"  Input files: {num_inputs}")
    print(f"  Total entries (pre-dedup): {stats['total_pre']}")
    print(f"  Duplicates resolved: {stats['duplicates_resolved']}")
    print(f"  Final entries: {stats['total_post']}")
    print(f"  By phase: {phase_str}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Merge JSONL insight databases from multiple research sessions, "
            "deduplicating by insight ID."
        ),
    )
    parser.add_argument(
        "--inputs", nargs="+", required=True,
        help="JSONL files to merge (space-separated list)",
    )
    parser.add_argument(
        "--output", required=True,
        help="Output JSONL file path",
    )
    parser.add_argument(
        "--strategy",
        choices=["newest", "highest_confidence", "manual"],
        default="newest",
        help=(
            "Deduplication strategy for unknown phases; "
            "manual emits conflict report (default: newest)"
        ),
    )
    parser.add_argument(
        "--dedup-by", default="id",
        help="Field to deduplicate on (default: id)",
    )
    args = parser.parse_args()

    # Validate input files
    for p in args.inputs:
        if not Path(p).exists():
            print(f"Error: input file not found: {p}", file=sys.stderr)
            sys.exit(1)

    merged, stats, conflicts = merge_sessions(
        args.inputs, args.strategy, args.dedup_by,
    )

    # ── Manual strategy – emit conflict report and exit ──
    if args.strategy == "manual":
        report = (
            {"status": "conflicts_found", "conflicts": conflicts}
            if conflicts
            else {"status": "no_conflicts"}
        )
        print(json.dumps(report, indent=2))
        sys.exit(0)

    # ── Write merged output ──
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for entry in merged:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print_summary(stats, len(args.inputs))


if __name__ == "__main__":
    main()