---
name: jupyter-autonomous-execution
description: Autonomous Jupyter notebook execution, error analysis, and systematic debugging across notebooks and Python modules
version: 1.0
---

# Jupyter Autonomous Execution & Debugging

> For use by Kilo AI coding assistant
> Enables autonomous execution of Jupyter notebooks and systematic debugging of errors across .ipynb and .py files

---

## IMPORTANT: Auto-Update Instruction

**To Kilo or any other coding agent:** If you discover new patterns, tools, or workflows for autonomous notebook execution and debugging, you MUST update this skill. Follow this process:

1. Test the new approach in real scenarios
2. Verify it works reliably
3. Add documentation following the existing format
4. Update the decision trees and integration sections
5. Commit with message: "docs: add <feature> to jupyter-autonomous-execution skill"

---

## Overview

This skill enables autonomous execution and debugging of Jupyter notebooks with systematic error analysis and iterative resolution. It handles:

- **Notebook Execution** - Run notebooks headlessly with output capture
- **Error Parsing** - Analyze Jupyter tracebacks and map to source
- **Cross-File Debugging** - Trace errors between notebooks and imported modules
- **Iterative Fixing** - Automated fix-and-retry loops
- **Validation** - Verify fixes with re-execution and tests

### When to Use This Skill

| Scenario | Activate This Skill | Reason |
|----------|--------------------|--------|
| Execute notebook for validation | ✅ | Run notebook and capture errors |
| Debug notebook execution error | ✅ | Parse traceback, locate, fix |
| Fix errors in imported modules | ✅ | Cross-file error resolution |
| Batch execute multiple notebooks | ✅ | Sequential execution with error tracking |
| Interactive exploration | ❌ | Use Jupyter UI directly |
| One-off cell execution | ❌ | Overhead not justified |
| Notebook requires user input | ❌ | Autonomous execution can't handle prompts |

---

## Tool Index

| Priority | Tool | Best For |
|----------|------|----------|
| Critical | `papermill` | Parameterized notebook execution |
| Critical | `nbconvert` | Notebook execution & conversion |
| Critical | `nbformat` | Programmatic notebook manipulation |
| Critical | `nbclient` | Notebook execution engine |
| High | `pytest` | Test validation for fixes |
| High | `rg` | Search notebook/cell content |
| High | `rga` | Search inside .ipynb files |
| Medium | `fd` | Find notebooks by name |
| Medium | `bat` | View notebook JSON with syntax |

---

## Installation

### Required Packages
```bash
# Install core execution tools with uv
uv add papermill nbconvert nbformat nbclient

# Or with pip (if not using pyproject.toml)
uv pip install papermill nbconvert nbformat nbclient

# For advanced execution features
uv pip install ipykernel jupyter
```

### Verify Installation
```bash
# Check papermill
uv run papermill --version

# Check nbconvert
uv run jupyter nbconvert --version

# Check nbformat
uv run python -c "import nbformat; print(nbformat.__version__)"
```

### Kernel Setup (if needed)
```bash
# Install current environment as Jupyter kernel
uv run python -m ipykernel install --user --name project-env --display-name "Project Env"

# List available kernels
uv run jupyter kernelspec list
```

---

## Tool Selection Guide

| Task | Tool | Command Pattern |
|------|------|-----------------|
| Execute notebook with parameters | `papermill` | `papermill input.ipynb output.ipynb -p param_name value` |
| Execute notebook for validation | `nbconvert --execute` | `jupyter nbconvert --to notebook --execute notebook.ipynb` |
| Execute and overwrite in place | `nbconvert --inplace` | `jupyter nbconvert --to notebook --execute --inplace notebook.ipynb` |
| Read notebook programmatically | `nbformat` | `nbformat.read(path, as_version=4)` |
| Find notebooks by name | `fd` | `fd -e ipynb pattern` |
| Search notebook content | `rga` | `rga "pattern" *.ipynb` |
| View notebook structure | `jq` | `cat notebook.ipynb \| jq '.cells[].source'` |
| Test fixed code | `pytest` | `uv run pytest tests/test_file.py` |
| Compare notebook diffs | `delta` | `git diff file.ipynb \| delta` |

---

## Execution Patterns

### Pattern 1: Simple Notebook Execution (Papermill)
```bash
# Execute notebook, save output to different file
uv run papermill input.ipynb output.ipynb

# Execute with parameters
uv run papermill input.ipynb output.ipynb -p epochs 100 -p lr 0.001

# Execute with multiple parameters
uv run papermill input.ipynb output.ipynb \
  -p param1 value1 \
  -p param2 value2 \
  -p flag_true true

# Execute with complex parameters (JSON)
uv run papermill input.ipynb output.ipynb \
  -p config '{"key": "value", "nested": {"a": 1}}'
```

### Pattern 2: Validation Execution (NbConvert)
```bash
# Execute and save to new notebook
uv run jupyter nbconvert --to notebook --execute input.ipynb --output output.ipynb

# Execute in place (overwrites original)
uv run jupyter nbconvert --to notebook --execute --inplace notebook.ipynb

# Execute with timeout (seconds)
uv run jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 notebook.ipynb

# Execute with specific kernel
uv run jupyter nbconvert --to notebook --execute --ExecutePreprocessor.kernel_name=python3 notebook.ipynb
```

### Pattern 3: Programmatic Execution (Python API)
```python
import nbformat
from nbclient import NotebookClient

# Read notebook
with open("notebook.ipynb", "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

# Execute
client = NotebookClient(nb, timeout=600, kernel_name="python3")
client.execute()

# Save executed notebook
with open("notebook_executed.ipynb", "w", encoding="utf-8") as f:
    nbformat.write(nb, f)
```

### Pattern 4: Papermill Python API
```python
import papermill as pm

# Execute with parameters
pm.execute_notebook(
    "input.ipynb",
    "output.ipynb",
    parameters={"epochs": 100, "lr": 0.001},
    kernel_name="python3",
    timeout=600,
)

# Execute and get report
report = pm.execute_notebook(
    "input.ipynb",
    "output.ipynb",
    parameters={"param": "value"},
    report_mode=True,
)
```

### Pattern 5: Batch Execution
```bash
# Execute all notebooks in directory
for file in notebooks/*.ipynb; do
    uv run papermill "$file" "output/${file##*/}" || echo "Failed: $file"
done

# Execute with error logging
uv run papermill notebook.ipynb output.ipynb 2> error.log || echo "Error logged"
```

---

## Error Parsing & Analysis

### Jupyter Error Structure
```json
{
  "cells": [
    {
      "cell_type": "code",
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "error",
          "ename": "NameError",
          "evalue": "name 'x' is not defined",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
            "Cell \u001b[0;32mIn[1], line 3\u001b[0m\n\u001b[0m      1 a = 1\u001b[0m\n\u001b[0;32m----> 3\u001b[0m \u001b[38;5;28mprint\u001b[39m(\u001b[43mx\u001b[49m)\n",
            "\u001b[0;31mNameError\u001b[0m: name 'x' is not defined"
          ]
        }
      ]
    }
  ]
}
```

### Error Type Classification

| Error Type | evalue Pattern | Likely Cause | Fix Strategy |
|------------|---------------|--------------|--------------|
| `NameError` | "name 'X' is not defined" | Missing variable/function definition | Define before use, check imports |
| `ModuleNotFoundError` | "No module named 'X'" | Missing package | `uv add X` or `uv pip install X` |
| `ImportError` | "cannot import name X from Y" | Wrong import or missing export | Fix import statement, check module |
| `SyntaxError` | "invalid syntax" | Syntax error in code | Fix syntax at indicated line |
| `KeyError` | "X" | Missing dict key | Add key or use .get() |
| `IndexError` | "list index out of range" | Invalid list/tuple index | Check bounds |
| `ValueError` | Various | Wrong value type/format | Validate input |
| `TypeError` | Various | Wrong type operation | Type check/convert |
| `FileNotFoundError` | "[Errno 2] No such file" | Missing file | Check path, create file |
| `AttributeError` | "'X' object has no attribute 'Y'" | Missing attribute/method | Check object type, method name |

### Parsing Traceback to Location
```python
import re

def parse_jupyter_traceback(traceback_lines):
    """
    Parse Jupyter traceback to extract error location.
    Returns: (cell_index, line_number, error_type, error_message)
    """
    error_info = {
        "cell_index": None,
        "line_number": None,
        "error_type": None,
        "error_message": None
    }
    
    cell_pattern = r"Cell In\[(\d+)\], line (\d+)"
    error_pattern = r"^(\w+):\s*(.+)$"
    
    for line in traceback_lines:
        # Extract cell and line number
        cell_match = re.search(cell_pattern, line)
        if cell_match:
            error_info["cell_index"] = int(cell_match.group(1))
            error_info["line_number"] = int(cell_match.group(2))
        
        # Extract error type and message
        error_match = re.match(error_pattern, line.strip())
        if error_match:
            error_info["error_type"] = error_match.group(1)
            error_info["error_message"] = error_match.group(2)
    
    return error_info
```

### Mapping Cell Index to Notebook
```python
import nbformat

def get_cell_source(notebook_path, cell_index):
    """Get source code of a specific cell."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    
    if 0 <= cell_index < len(nb.cells):
        cell = nb.cells[cell_index]
        if cell.cell_type == "code":
            return "".join(cell.source)
    return None

def find_cell_by_content(notebook_path, search_pattern):
    """Find cell index containing specific content."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    
    import re
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "code":
            if re.search(search_pattern, "".join(cell.source)):
                return i
    return None
```

---

## Debugging Workflow

### Workflow 1: Single Error Resolution
```
1. Execute notebook → Capture error
2. Parse traceback → Extract cell_index, line_number, error_type
3. Locate source → Read cell source code
4. Analyze error → Determine root cause
5. Apply fix → Modify cell source
6. Re-execute → Validate fix
7. If still failing → Loop to step 2
```

### Workflow 2: Cross-File Error Resolution
```
1. Execute notebook → Error in imported module
2. Parse traceback → Extract module name, file path, line
3. Read source file → Locate error in .py file
4. Apply fix → Edit source file
5. Re-execute notebook → Validate fix
6. Run tests → Ensure no regression
```

### Workflow 3: Batch Notebook Validation
```
For each notebook in batch:
  1. Execute with papermill
  2. If success → Mark as PASSED
  3. If failure → 
     a. Parse error
     b. Categorize (dependency/syntax/logic)
     c. Queue for fixing
  4. Generate report (passed/failed/error_summary)
```

---

## Integration with Existing Tools

### Search & Locate
```bash
# Find notebook by name
fd -e ipynb "pattern"

# Search content across all notebooks
rga "function_name" notebooks/

# Find notebooks containing specific import
rga "^import pandas|^from pandas" notebooks/

# View notebook structure
bat notebook.ipynb

# View specific cell range
cat notebook.ipynb | jq '.cells[0:5].source'
```

### Compare & Diff
```bash
# Compare notebook versions (before/after fix)
delta original.ipynb fixed.ipynb

# Show git diff with pretty formatting
git diff notebook.ipynb | delta

# Extract source only for comparison
jq '.cells[] | select(.cell_type=="code") | .source' file1.ipynb > src1.txt
jq '.cells[] | select(.cell_type=="code") | .source' file2.ipynb > src2.txt
diff src1.txt src2.txt
```

### Test Validation
```bash
# Run tests after fix
uv run pytest tests/test_module.py -v

# Run specific test
uv run pytest tests/test_module.py::test_function_name -v

# Run with coverage
uv run pytest --cov=src tests/
```

---

## Common Scenarios & Solutions

### Scenario 1: ModuleNotFoundError
```python
# Error: ModuleNotFoundError: No module named 'sklearn'

# Solution: Install missing package
uv add scikit-learn

# Or with pip
uv pip install scikit-learn

# Verify
uv run python -c "import sklearn; print(sklearn.__version__)"

# Re-execute notebook
uv run papermill notebook.ipynb output.ipynb
```

### Scenario 2: NameError in Cell
```python
# Cell 1:
model = RandomForestClassifier()

# Cell 2:
model.fit(X, y)  # NameError: name 'X' is not defined

# Solution: Ensure X, y are defined before use
# Check if X, y defined in previous cells
# Or define in current cell:
X = df[features]
y = df[target]
model.fit(X, y)
```

### Scenario 3: SyntaxError in Imported Module
```python
# Error in src/patterns/detector.py line 45
# SyntaxError: invalid syntax

# Solution:
# 1. Read source file
bat src/patterns/detector.py --line-range 40:50

# 2. Fix syntax error
edit src/patterns/detector.py

# 3. Run tests
uv run pytest tests/test_detector.py

# 4. Re-execute notebook
uv run papermill notebook.ipynb output.ipynb
```

### Scenario 4: ImportError - Circular Dependency
```python
# Error: ImportError: cannot import name 'X' from 'Y'

# Likely circular import. Solution:
# Option 1: Move import inside function (lazy import)
def func():
    from module import X  # Import when needed

# Option 2: Restructure modules to break cycle
# Option 3: Use TYPE_CHECKING for type hints only
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from module import X
```

### Scenario 5: Cell Execution Order Issue
```python
# Error occurs because cells executed out of order

# Solution with papermill:
# Reorder cells or mark execution order
import nbformat

with open("notebook.ipynb", "r") as f:
    nb = nbformat.read(f, as_version=4)

# Check execution counts
for i, cell in enumerate(nb.cells):
    if cell.cell_type == "code":
        print(f"Cell {i}: execution_count = {cell.execution_count}")

# Cells should be executed in numeric order of execution_count
```

---

## Decision Tree

```
Start: Need to debug notebook
│
├─ Error in notebook cell?
│  ├─ Yes → Execute with papermill, capture output
│  │        ├─ Parse traceback
│  │        ├─ Is error in notebook cell?
│  │        │  ├─ Yes → Fix cell source, re-execute
│  │        │  └─ No (error in imported module) → Go to "Error in .py file"
│  │        └─ Repeat until success
│  │
│  └─ No → Execute to validate
│           └─ Use nbconvert --execute
│
├─ Error in imported .py file?
│  ├─ Parse traceback → Extract file path, line number
│  ├─ Read source file → bat/rscope shows context
│  ├─ Apply fix → Edit file
│  ├─ Run tests → pytest
│  └─ Re-execute notebook → Validate
│
├─ Finding which notebook has issue?
│  ├─ Batch execute with error logging
│  ├─ Parse error logs → Identify failing notebooks
│  └─ Process each failure individually
│
└─ Notebook won't execute due to dependencies?
   ├─ Check requirements → pip list / uv pip list
   ├─ Install missing → uv add <package>
   ├─ Check kernel → jupyter kernelspec list
   └─ Re-execute
```

---

## Anti-Patterns: When NOT to Use This Skill

| Scenario | Why Not | Alternative |
|----------|---------|-------------|
| Interactive data exploration | Autonomous execution too rigid | Use Jupyter UI directly |
| Notebook requires user input | Can't handle `input()` prompts | Use Jupyter UI or refactor |
| Visual debugging needed | Can't see plots/outputs interactively | Use Jupyter UI |
| One-time cell fix | Overhead not justified | Fix manually in UI |
| Exploratory prototype | Requirements change too fast | Use Jupyter UI first, then automate |
| Notebook has widgets/interactivity | ipywidgets don't work headless | Use Jupyter UI |
| Need to see intermediate outputs | Autonomous execution runs to end | Use Jupyter UI or add logging |

---

## Advanced Patterns

### Pattern: Extract All Errors from Notebook
```python
import nbformat

def extract_errors(notebook_path):
    """Extract all errors from an executed notebook."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    
    errors = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "code":
            for output in cell.outputs:
                if output.output_type == "error":
                    errors.append({
                        "cell_index": i,
                        "error_type": output.ename,
                        "error_message": output.evalue,
                        "traceback": output.traceback
                    })
    return errors
```

### Pattern: Retry Failed Cells
```python
import nbformat
from nbclient import NotebookClient

def retry_failed_cells(notebook_path, max_retries=3):
    """Retry execution of failed cells."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    
    failed_cells = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "code":
            for output in cell.outputs:
                if output.output_type == "error":
                    failed_cells.append(i)
                    break
    
    # Clear failed cell outputs and re-execute
    for i in failed_cells:
        nb.cells[i].outputs = []
        nb.cells[i].execution_count = None
    
    # Re-execute
    client = NotebookClient(nb, timeout=600, kernel_name="python3")
    client.execute()
    
    return nb
```

### Pattern: Compare Notebook Executions
```python
import nbformat

def compare_executions(nb1_path, nb2_path):
    """Compare cell outputs between two executed notebooks."""
    with open(nb1_path, "r") as f:
        nb1 = nbformat.read(f, as_version=4)
    with open(nb2_path, "r") as f:
        nb2 = nbformat.read(f, as_version=4)
    
    differences = []
    for i, (c1, c2) in enumerate(zip(nb1.cells, nb2.cells)):
        if c1.cell_type == "code" and c2.cell_type == "code":
            # Compare execution outputs
            if len(c1.outputs) != len(c2.outputs):
                differences.append(f"Cell {i}: different output count")
            # Compare execution success
            for o1, o2 in zip(c1.outputs, c2.outputs):
                if o1.output_type != o2.output_type:
                    differences.append(f"Cell {i}: different output type")
    
    return differences
```

---

## Troubleshooting

### Issue: Papermill hangs during execution
```bash
# Solution: Add timeout
uv run papermill input.ipynb output.ipynb --request-save-on-cell-execute false
# Or set environment variable
export PAPERMILL_REQUEST_TIMEOUT=600
```

### Issue: Kernel not found
```bash
# List available kernels
uv run jupyter kernelspec list

# Install kernel if missing
uv run python -m ipykernel install --user --name python3

# Or use nbconvert Python API with specific kernel
```

### Issue: Notebook uses different Python version
```bash
# Check notebook kernel spec
jq '.metadata.kernelspec' notebook.ipynb

# Reinstall kernel with current Python
uv run python -m ipykernel install --user --name project-env

# Update notebook to use correct kernel
jq '.metadata.kernelspec.name = "project-env"' notebook.ipynb > tmp.ipynb && mv tmp.ipynb notebook.ipynb
```

### Issue: Cell execution order wrong
```bash
# Papermill executes top to bottom by default
# If cell dependencies are wrong, reorder cells in notebook
# Or use tags to mark execution order

# Extract cells to check order
jq '.cells[] | {cell_type, execution_count, source: .source[0:50]}' notebook.ipynb
```

---

## Quick Reference

### One-Liners
```bash
# Execute notebook
uv run papermill in.ipynb out.ipynb

# Execute and validate
uv run jupyter nbconvert --to notebook --execute --inplace notebook.ipynb

# Find notebook with error
fd -e ipynb | xargs -I {} uv run papermill {} /tmp/test.ipynb 2>&1 | grep -l "Error"

# Search for function in notebooks
rga "def my_function" notebooks/

# View cell source
jq '.cells[3].source' notebook.ipynb

# Run all tests
uv run pytest tests/ -v

# Check notebook JSON validity
jq '.' notebook.ipynb > /dev/null && echo "Valid JSON"
```

### Common Fixes
```python
# Fix 1: Install missing package
uv add package_name

# Fix 2: Import at top of cell
import module_name

# Fix 3: Define variable before use
variable = default_value

# Fix 4: Check file exists
from pathlib import Path
Path("file.csv").exists()

# Fix 5: Validate data shape
df.shape  # Should match expected (rows, cols)
```

---

## Activation Modes

This skill operates in two modes: **Manual** (default) and **Autonomous**.

### Quick Toggle

```bash
# Enable autonomous mode
uv run scripts/toggle_autonomous.py --enable

# Disable autonomous mode
uv run scripts/toggle_autonomous.py --disable

# Check current status
uv run scripts/toggle_autonomous.py --status

# Programmatic check (exit code 0 if enabled)
uv run scripts/toggle_autonomous.py --check
```

### Mode Comparison

| Mode | AI Behavior | When to Use |
|------|-------------|-------------|
| **Manual** (default) | Execute notebooks only when explicitly requested | Safe, controlled execution |
| **Autonomous** | Auto-execute and debug when notebook errors detected | Active notebook development |

### Autonomous Mode Behavior

When **ENABLED**, the AI will automatically:

1. **Detect** - Monitor for notebook errors when `.ipynb` files change
2. **Execute** - Run notebooks to capture full error context
3. **Parse** - Extract error type, location, and root cause
4. **Fix** - Apply auto-fix based on error type:
   - `ModuleNotFoundError` → `uv add <package>`
   - `NameError` → Search and add missing definition
   - `SyntaxError` → Fix syntax at indicated line
   - `ImportError` → Correct import path
   - `FileNotFoundError` → Verify/create path
5. **Validate** - Re-execute to confirm fix
6. **Iterate** - Up to `max_retry_iterations` (default: 5)

### Activation Checks

The AI checks these in order:

1. `config.json` → `enabled` field
2. Environment variable → `JUPYTER_AUTONOMOUS_ENABLED=true`
3. Project marker file → `.jupyter-autonomous-enabled`

### Configuration

Edit `config.json` to customize:

```json
{
  "enabled": false,
  "auto_execute_on_error": true,
  "max_retry_iterations": 5,
  "timeout_per_execution": 600,
  "auto_fix_patterns": {
    "ModuleNotFoundError": "install_package",
    "NameError": "check_definition",
    "SyntaxError": "fix_syntax",
    "FileNotFoundError": "check_path"
  },
  "safety": {
    "require_confirmation_for_package_install": true,
    "max_concurrent_executions": 1
  }
}
```

### Safety Guidelines

- Autonomous mode **never** runs outside `allowed_notebook_patterns`
- Package installations require confirmation (configurable)
- Maximum one notebook execution at a time
- All executions logged to `reporting.output_directory`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-04-21 | Added activation toggle system |
| 1.0 | 2026-04-21 | Initial release |

---

## Related Skills

- `cli-tools` - For rg, rga, fd, bat, jq used in search/view operations
- `mcp-search-strategy` - For finding code patterns across notebooks and modules
