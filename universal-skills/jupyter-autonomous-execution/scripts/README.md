# Jupyter Autonomous Execution Scripts

This directory contains helper scripts for notebook execution and debugging.

## Scripts Overview

| Script | Purpose | Example Usage |
|--------|---------|---------------|
| `execute_notebook.py` | Execute single notebook with error capture | `uv run execute_notebook.py notebook.ipynb output.ipynb` |
| `parse_errors.py` | Parse errors from executed notebook | `uv run parse_errors.py executed.ipynb --json` |
| `batch_execute.py` | Execute multiple notebooks, generate report | `uv run batch_execute.py notebooks/*.ipynb` |
| `view_cells.py` | View/compare notebook cells | `uv run view_cells.py notebook.ipynb --cell 3` |

---

## Script Details

### execute_notebook.py

Execute a Jupyter notebook and save the output with execution results.

**Options:**
```bash
# Basic execution
uv run scripts/execute_notebook.py input.ipynb output.ipynb

# Execute and overwrite original
uv run scripts/execute_notebook.py notebook.ipynb --inplace

# Custom timeout (seconds)
uv run scripts/execute_notebook.py notebook.ipynb output.ipynb --timeout 1200

# Custom kernel
uv run scripts/execute_notebook.py notebook.ipynb output.ipynb --kernel python3
```

**Output (JSON):**
```json
{
  "success": true,
  "output_file": "output.ipynb",
  "executed_cells": 15,
  "errors": []
}
```

---

### parse_errors.py

Extract and analyze errors from an executed notebook.

**Options:**
```bash
# Human-readable report
uv run scripts/parse_errors.py executed.ipynb

# JSON output for programmatic use
uv run scripts/parse_errors.py executed.ipynb --json

# Include full traceback
uv run scripts/parse_errors.py executed.ipynb --verbose

# Get errors from specific cell
uv run scripts/parse_errors.py executed.ipynb --cell 5
```

**Output (text):**
```
Found 2 error(s):

--- Error 1 ---
Cell: 3
Type: NameError
Message: name 'X' is not defined

--- Error 2 ---
Cell: 7
Type: ModuleNotFoundError
Message: No module named 'sklearn'
```

**Output (JSON):**
```json
[
  {
    "cell_index": 3,
    "execution_count": 3,
    "error_type": "NameError",
    "error_message": "name 'X' is not defined",
    "parsed": {
      "cell_index": 3,
      "line_number": 5,
      "error_type": "NameError"
    }
  }
]
```

---

### batch_execute.py

Execute multiple notebooks and generate aggregate report.

**Options:**
```bash
# Execute all notebooks matching pattern
uv run scripts/batch_execute.py notebooks/*.ipynb --output report.json

# Execute with output directory
uv run scripts/batch_execute.py notebooks/*.ipynb -d executed/

# Print summary only
uv run scripts/batch_execute.py notebooks/*.ipynb --summary

# Custom timeout per notebook
uv run scripts/batch_execute.py notebooks/*.ipynb --timeout 900
```

**Summary Output:**
```
============================================================
Batch Execution Summary
============================================================
Total:      10
Successful: 8
Failed:     2
Success Rate: 80.0%
```

---

### view_cells.py

View and compare notebook cells.

**Options:**
```bash
# View all cells
uv run scripts/view_cells.py notebook.ipynb

# View specific cell
uv run scripts/view_cells.py notebook.ipynb --cell 3

# View multiple cells
uv run scripts/view_cells.py notebook.ipynb --cell 1 --cell 3 --cell 5

# Show cell outputs
uv run scripts/view_cells.py notebook.ipynb --output

# Compare two notebooks
uv run scripts/view_cells.py nb1.ipynb nb2.ipynb --diff

# JSON output
uv run scripts/view_cells.py notebook.ipynb --json
```

---

## Integration with Workflows

### CI/CD Pipeline Example
```yaml
# .github/workflows/notebook-test.yml
- name: Execute notebooks
  run: |
    uv run scripts/batch_execute.py notebooks/*.ipynb --output report.json
    
- name: Check for failures
  run: |
    uv run scripts/parse_errors.py executed/notebook.ipynb
```

### Debug Loop Example
```bash
#!/bin/bash
# debug_loop.sh

NOTEBOOK=$1
MAX_ITERATIONS=5

for i in $(seq 1 $MAX_ITERATIONS); do
    echo "=== Iteration $i ==="
    
    # Execute
    uv run scripts/execute_notebook.py "$NOTEBOOK" --inplace
    
    # Parse errors
    ERRORS=$(uv run scripts/parse_errors.py "$NOTEBOOK" --json)
    
    # Check if fixed
    if echo "$ERRORS" | jq -e 'length == 0' > /dev/null; then
        echo "All errors resolved!"
        exit 0
    fi
    
    # Auto-fix based on error type
    ERROR_TYPE=$(echo "$ERRORS" | jq -r '.[0].error_type')
    case "$ERROR_TYPE" in
        "ModuleNotFoundError")
            MODULE=$(echo "$ERRORS" | jq -r '.[0].error_message' | sed "s/No module named '\(.*\)'/\1/")
            uv add "$MODULE"
            ;;
        # Add more auto-fix patterns...
    esac
done

echo "Max iterations reached"
exit 1
```

---

## Programmatic Usage

### Python API Example
```python
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from execute_notebook import execute_notebook
from parse_errors import extract_errors

# Execute notebook
result = execute_notebook("input.ipynb", "output.ipynb")

if not result["success"]:
    # Parse errors
    errors = extract_errors(result["output_file"])
    
    for error in errors:
        print(f"Cell {error['cell_index']}: {error['error_type']}")
        print(f"  {error['error_message']}")
```

---

## Troubleshooting

### Script not found
```bash
# Make sure you're running from skill directory
cd C:\Dev\skills\jupyter-autonomous-execution

# Or use full path
uv run C:\Dev\skills\jupyter-autonomous-execution\scripts\execute_notebook.py ...
```

### Missing dependencies
```bash
# Install required packages
uv add nbformat nbclient nbconvert papermill
```

### Permission issues
```bash
# Scripts don't need execute permission when run with uv run
# But if needed:
chmod +x scripts/*.py  # On Unix-like systems
```
