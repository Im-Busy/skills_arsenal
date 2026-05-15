# Jupyter Autonomous Execution Skill

Autonomous execution and systematic debugging of Jupyter notebooks.

## Quick Start

### 1. Install Dependencies

```bash
uv add papermill nbconvert nbformat nbclient
```

### 2. Toggle Autonomous Mode

```bash
# Enable autonomous execution (auto-debug on errors)
uv run scripts/toggle_autonomous.py --enable

# Disable (manual mode - only runs when asked)
uv run scripts/toggle_autonomous.py --disable

# Check current status
uv run scripts/toggle_autonomous.py --status
```

### 3. Execute a Notebook

```bash
# Using papermill directly
uv run papermill notebook.ipynb output.ipynb

# Using the custom execute script
uv run scripts/execute_notebook.py notebook.ipynb output.ipynb
```

### 4. Parse Errors (if any)

```bash
# Human-readable report
uv run scripts/parse_errors.py output.ipynb

# JSON format for programmatic use
uv run scripts/parse_errors.py output.ipynb --json
```

### 5. View Problematic Cells

```bash
# View specific cell
uv run scripts/view_cells.py output.ipynb --cell 3
```

### 6. Fix and Re-execute

Apply fixes based on error analysis, then re-execute until success.

---

## Activation Modes

| Mode | Description | Toggle |
|------|-------------|--------|
| **Manual** (default) | Execute only when explicitly asked | `--disable` |
| **Autonomous** | Auto-execute and debug on errors | `--enable` |

When autonomous mode is ON, the AI will:
- Detect notebook errors when `.ipynb` files change
- Execute notebooks to capture errors
- Parse and auto-fix common error patterns
- Re-execute to validate fixes
- Iterate up to 5 times by default

---

## Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation with workflows and patterns
- **[ACTIVATION.md](ACTIVATION.md)** - Detailed activation mode guide
- **[scripts/README.md](scripts/README.md)** - Script usage guide
- **[templates/README.md](templates/README.md)** - Debugging workflow templates
- **[.useful_commands/useful_commands.txt](.useful_commands/useful_commands.txt)** - Quick command reference

---

## Common Workflows

### Debug Loop

```bash
# 1. Execute
uv run scripts/execute_notebook.py notebook.ipynb output.ipynb

# 2. Parse errors
uv run scripts/parse_errors.py output.ipynb --json

# 3. View problematic cell
uv run scripts/view_cells.py output.ipynb --cell {index}

# 4. Fix (edit cell source)

# 5. Re-execute (goto step 1)
```

### Batch Validation

```bash
# Execute all notebooks and generate report
uv run scripts/batch_execute.py notebooks/*.ipynb --output report.json --summary
```

---

## Error Resolution Quick Reference

| Error Type | Typical Fix |
|------------|-------------|
| `ModuleNotFoundError` | `uv add <package_name>` |
| `NameError` | Define variable before use |
| `SyntaxError` | Fix syntax at indicated line |
| `ImportError` | Check import path and exports |
| `KeyError` | Add key or use `.get()` |
| `FileNotFoundError` | Verify or create file path |

---

## Integration

This skill integrates with:
- **cli-tools** skill for `rg`, `rga`, `fd`, `bat` operations
- **Project test suite** via `pytest`
- **Git workflows** for version control

---

## Version

1.1 (2026-04-21)
