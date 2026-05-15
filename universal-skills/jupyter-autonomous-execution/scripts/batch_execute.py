#!/usr/bin/env python3
"""
Batch execute multiple notebooks and generate a report.

Usage:
    uv run batch_execute.py notebooks/ --output report.json
    uv run batch_execute.py *.ipynb --output-dir executed/
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def execute_single(notebook_path, timeout=600, kernel_name="python3"):
    """Execute a single notebook and return results."""
    result = {
        "notebook": str(notebook_path),
        "success": False,
        "errors": [],
        "executed_cells": 0,
        "duration": None,
    }

    try:
        with open(notebook_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        start_time = datetime.now()
        client = NotebookClient(nb, timeout=timeout, kernel_name=kernel_name)
        client.execute()
        end_time = datetime.now()

        result["duration"] = (end_time - start_time).total_seconds()

        for i, cell in enumerate(nb.cells):
            if cell.cell_type == "code":
                result["executed_cells"] += 1
                for output in cell.outputs:
                    if output.output_type == "error":
                        result["errors"].append(
                            {
                                "cell_index": i,
                                "error_type": output.ename,
                                "error_message": output.evalue,
                            }
                        )

        result["success"] = len(result["errors"]) == 0

    except Exception as e:
        result["errors"].append(
            {
                "error_type": type(e).__name__,
                "error_message": str(e),
            }
        )

    return result


def batch_execute(notebook_paths, output_dir=None, timeout=600):
    """Execute multiple notebooks and return aggregate results."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "total": len(notebook_paths),
        "successful": 0,
        "failed": 0,
        "notebooks": [],
    }

    for path in notebook_paths:
        print(f"Executing: {path}", file=sys.stderr)

        result = execute_single(path, timeout=timeout)
        results["notebooks"].append(result)

        if result["success"]:
            results["successful"] += 1
            print(f"  ✓ Success", file=sys.stderr)
        else:
            results["failed"] += 1
            print(f"  ✗ Failed: {len(result['errors'])} error(s)", file=sys.stderr)

        if output_dir:
            output_path = Path(output_dir) / Path(path).name
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                nb = nbformat.read(path, as_version=4)
                try:
                    client = NotebookClient(nb, timeout=timeout)
                    client.execute()
                except Exception:
                    pass
                nbformat.write(nb, f)

    results["success_rate"] = (
        results["successful"] / results["total"] if results["total"] > 0 else 0
    )

    return results


def main():
    parser = argparse.ArgumentParser(description="Batch execute Jupyter notebooks")
    parser.add_argument("notebooks", nargs="+", help="Notebook paths or glob pattern")
    parser.add_argument("--output", "-o", help="Output report path (JSON)")
    parser.add_argument("--output-dir", "-d", help="Directory for executed notebooks")
    parser.add_argument("--timeout", "-t", type=int, default=600, help="Timeout per notebook")
    parser.add_argument("--summary", action="store_true", help="Print summary only")

    args = parser.parse_args()

    notebook_files = []
    for pattern in args.notebooks:
        notebook_files.extend(Path(".").glob(pattern) if "*" in pattern else [Path(pattern)])

    notebook_files = [f for f in notebook_files if f.exists() and f.suffix == ".ipynb"]

    if not notebook_files:
        print("No notebooks found", file=sys.stderr)
        sys.exit(1)

    results = batch_execute(notebook_files, args.output_dir, args.timeout)

    if args.summary:
        print(f"\n{'=' * 60}")
        print(f"Batch Execution Summary")
        print(f"{'=' * 60}")
        print(f"Total:      {results['total']}")
        print(f"Successful: {results['successful']}")
        print(f"Failed:     {results['failed']}")
        print(f"Success Rate: {results['success_rate'] * 100:.1f}%")
    else:
        print(json.dumps(results, indent=2))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"\nReport saved to: {args.output}", file=sys.stderr)

    sys.exit(0 if results["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
