#!/usr/bin/env python3
"""
Execute a Jupyter notebook and capture errors.

Usage:
    uv run execute_notebook.py notebook.ipynb output.ipynb
    uv run execute_notebook.py notebook.ipynb --inplace
    uv run execute_notebook.py notebook.ipynb output.ipynb --timeout 600
"""

import argparse
import json
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbconvert.preprocessors import ExecutePreprocessor


def execute_notebook(
    input_path: str,
    output_path: str = None,
    inplace: bool = False,
    timeout: int = 600,
    kernel_name: str = "python3",
):
    """
    Execute a Jupyter notebook and save the output.

    Args:
        input_path: Path to input notebook
        output_path: Path to output notebook (optional if inplace)
        inplace: If True, overwrite input file
        timeout: Execution timeout in seconds
        kernel_name: Kernel to use for execution

    Returns:
        dict with execution results
    """
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Notebook not found: {input_path}")

    # Determine output path
    if inplace:
        output_file = input_file
    elif output_path:
        output_file = Path(output_path)
    else:
        output_file = input_file.with_name(f"{input_file.stem}_executed{input_file.suffix}")

    # Read notebook
    with open(input_file, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # Execute
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name=kernel_name,
        record_timing=True,
    )

    errors = []
    executed_cells = []

    try:
        client.execute()

        # Track which cells executed and which had errors
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == "code":
                executed_cells.append(i)
                for output in cell.outputs:
                    if output.output_type == "error":
                        errors.append(
                            {
                                "cell_index": i,
                                "error_type": output.ename,
                                "error_message": output.evalue,
                            }
                        )

    except Exception as e:
        # Execution failed partway through
        print(f"Execution error: {e}", file=sys.stderr)

    # Save output
    with open(output_file, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)

    return {
        "success": len(errors) == 0,
        "output_file": str(output_file),
        "executed_cells": len(executed_cells),
        "errors": errors,
    }


def main():
    parser = argparse.ArgumentParser(description="Execute a Jupyter notebook")
    parser.add_argument("input", help="Input notebook path")
    parser.add_argument("output", nargs="?", help="Output notebook path (optional)")
    parser.add_argument("--inplace", action="store_true", help="Overwrite input file")
    parser.add_argument("--timeout", type=int, default=600, help="Execution timeout (seconds)")
    parser.add_argument("--kernel", default="python3", help="Kernel name")

    args = parser.parse_args()

    if args.inplace and args.output:
        print("Error: Cannot specify both --inplace and output path", file=sys.stderr)
        sys.exit(1)

    result = execute_notebook(
        args.input,
        args.output,
        args.inplace,
        args.timeout,
        args.kernel,
    )

    # Print results
    print(json.dumps(result, indent=2))

    # Exit with error code if execution failed
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
