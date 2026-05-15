#!/usr/bin/env python3
"""
View and compare notebook cells.

Usage:
    uv run view_cells.py notebook.ipynb
    uv run view_cells.py notebook.ipynb --cell 3
    uv run view_cells.py notebook1.ipynb notebook2.ipynb --diff
"""

import argparse
import json
import sys
from pathlib import Path

import nbformat


def get_cell_source(cell):
    """Get cell source as string."""
    if isinstance(cell.source, list):
        return "".join(cell.source)
    return cell.source


def view_cells(notebook_path, cell_indices=None, show_code=True, show_output=False):
    """View specific cells or all cells from a notebook."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    code_cells = [c for c in nb.cells if c.cell_type == "code"]

    if cell_indices is None:
        cell_indices = range(len(code_cells))

    results = []
    for i in cell_indices:
        if 0 <= i < len(code_cells):
            cell = code_cells[i]
            cell_info = {
                "index": i,
                "execution_count": cell.execution_count,
                "source": get_cell_source(cell),
            }

            if show_output and cell.outputs:
                cell_info["outputs"] = []
                for output in cell.outputs:
                    if output.output_type == "stream":
                        cell_info["outputs"].append({"type": "stream", "text": output.text})
                    elif output.output_type == "execute_result":
                        cell_info["outputs"].append(
                            {
                                "type": "execute_result",
                                "data": output.data.get("text/plain", ""),
                            }
                        )
                    elif output.output_type == "error":
                        cell_info["outputs"].append(
                            {
                                "type": "error",
                                "ename": output.ename,
                                "evalue": output.evalue,
                            }
                        )

            results.append(cell_info)

    return results


def compare_cells(nb1_path, nb2_path):
    """Compare cells between two notebooks."""
    with open(nb1_path, "r", encoding="utf-8") as f:
        nb1 = nbformat.read(f, as_version=4)
    with open(nb2_path, "r", encoding="utf-8") as f:
        nb2 = nbformat.read(f, as_version=4)

    code1 = [c for c in nb1.cells if c.cell_type == "code"]
    code2 = [c for c in nb2.cells if c.cell_type == "code"]

    comparison = {
        "nb1_cells": len(code1),
        "nb2_cells": len(code2),
        "differences": [],
    }

    max_len = max(len(code1), len(code2))
    for i in range(max_len):
        if i >= len(code1):
            comparison["differences"].append(
                {
                    "cell": i,
                    "status": "missing_in_nb1",
                }
            )
        elif i >= len(code2):
            comparison["differences"].append(
                {
                    "cell": i,
                    "status": "missing_in_nb2",
                }
            )
        else:
            src1 = get_cell_source(code1[i])
            src2 = get_cell_source(code2[i])
            if src1 != src2:
                comparison["differences"].append(
                    {
                        "cell": i,
                        "status": "different",
                        "nb1_lines": len(src1.splitlines()),
                        "nb2_lines": len(src2.splitlines()),
                    }
                )

    return comparison


def main():
    parser = argparse.ArgumentParser(description="View notebook cells")
    parser.add_argument("notebooks", nargs="+", help="Notebook path(s)")
    parser.add_argument("--cell", "-c", type=int, action="append", help="Specific cell index")
    parser.add_argument("--no-code", action="store_true", help="Hide cell source")
    parser.add_argument("--output", "-o", action="store_true", help="Show cell outputs")
    parser.add_argument("--diff", action="store_true", help="Compare two notebooks")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.diff:
        if len(args.notebooks) != 2:
            print("Error: --diff requires exactly two notebooks", file=sys.stderr)
            sys.exit(1)

        result = compare_cells(args.notebooks[0], args.notebooks[1])

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Notebook 1: {args.notebooks[0]} ({result['nb1_cells']} cells)")
            print(f"Notebook 2: {args.notebooks[1]} ({result['nb2_cells']} cells)")
            print(f"\nDifferences: {len(result['differences'])}")
            for diff in result["differences"][:10]:
                print(f"  Cell {diff['cell']}: {diff['status']}")

        sys.exit(0)

    # Single notebook view
    for nb_path in args.notebooks:
        cells = view_cells(nb_path, args.cell, args.no_code is False, args.output)

        if args.json:
            print(json.dumps(cells, indent=2))
        else:
            for cell in cells:
                print(f"\n{'=' * 60}")
                print(f"Cell {cell['index']} (execution: {cell['execution_count']})")
                print(f"{'=' * 60}")
                if not args.no_code:
                    print(
                        cell["source"][:500] + "..."
                        if len(cell["source"]) > 500
                        else cell["source"]
                    )
                if args.output and cell.get("outputs"):
                    print("\nOutputs:")
                    for out in cell["outputs"]:
                        if out["type"] == "error":
                            print(f"  ERROR: {out['ename']}: {out['evalue']}")

    sys.exit(0)


if __name__ == "__main__":
    main()
