#!/usr/bin/env python3
"""
Parse Jupyter notebook errors from execution output.

Usage:
    uv run parse_errors.py executed_notebook.ipynb
    uv run parse_errors.py executed_notebook.ipynb --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

import nbformat


def parse_traceback(traceback_lines):
    """Parse Jupyter traceback to extract error location."""
    error_info = {
        "cell_index": None,
        "line_number": None,
        "error_type": None,
        "error_message": None,
        "file_path": None,
    }

    cell_pattern = r"Cell In\[(\d+)\], line (\d+)"
    file_pattern = r"File ([^:]+):(\d+)"
    error_pattern = r"^(\w+):\s*(.+)$"

    for line in traceback_lines:
        cell_match = re.search(cell_pattern, line)
        if cell_match:
            error_info["cell_index"] = int(cell_match.group(1))
            error_info["line_number"] = int(cell_match.group(2))

        file_match = re.search(file_pattern, line)
        if file_match:
            error_info["file_path"] = file_match.group(1)
            error_info["line_number"] = int(file_match.group(2))

        error_match = re.match(error_pattern, line.strip())
        if error_match:
            error_info["error_type"] = error_match.group(1)
            error_info["error_message"] = error_match.group(2)

    return error_info


def extract_errors(notebook_path):
    """Extract all errors from an executed notebook."""
    nb_path = Path(notebook_path)

    if not nb_path.exists():
        raise FileNotFoundError(f"Notebook not found: {notebook_path}")

    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    errors = []

    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "code":
            for output in cell.outputs:
                if output.output_type == "error":
                    error_info = parse_traceback(output.traceback)
                    errors.append(
                        {
                            "cell_index": i,
                            "execution_count": cell.execution_count,
                            "error_type": output.ename,
                            "error_message": output.evalue,
                            "traceback": output.traceback,
                            "parsed": error_info,
                        }
                    )

    return errors


def format_error_report(errors, verbose=False):
    """Format errors as human-readable report."""
    if not errors:
        return "No errors found."

    report = []
    report.append(f"Found {len(errors)} error(s):\n")

    for i, err in enumerate(errors, 1):
        report.append(f"--- Error {i} ---")
        report.append(f"Cell: {err['cell_index']}")
        report.append(f"Type: {err['error_type']}")
        report.append(f"Message: {err['error_message']}")

        if err.get("parsed", {}).get("file_path"):
            report.append(f"File: {err['parsed']['file_path']}")

        if verbose and err.get("traceback"):
            report.append("Traceback:")
            for line in err["traceback"][-5:]:
                report.append(f"  {line}")

        report.append("")

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Parse errors from executed notebook")
    parser.add_argument("notebook", help="Executed notebook path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Include full traceback")
    parser.add_argument("--cell", type=int, help="Get errors from specific cell")

    args = parser.parse_args()

    try:
        errors = extract_errors(args.notebook)

        if args.cell is not None:
            errors = [e for e in errors if e["cell_index"] == args.cell]

        if args.json:
            print(json.dumps(errors, indent=2))
        else:
            print(format_error_report(errors, args.verbose))

        sys.exit(0 if not errors else 1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
