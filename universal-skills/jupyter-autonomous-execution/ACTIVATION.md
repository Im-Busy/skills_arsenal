# Jupyter Autonomous Execution - Activation Guide

## Overview

This skill can operate in two modes:

| Mode | Description | When to Use |
|------|-------------|-------------|
| **Manual** | AI executes notebooks only when explicitly requested | Default, safe mode |
| **Autonomous** | AI automatically executes and debugs notebooks when errors detected | Active development with frequent notebook changes |

---

## Quick Toggle

### Enable Autonomous Mode

```bash
# Method 1: Use the toggle script
uv run scripts/toggle_autonomous.py --enable

# Method 2: Edit config directly
jq '.enabled = true' config.json > tmp.json && mv tmp.json config.json

# Method 3: Set environment variable (session only)
set JUPTYER_AUTONOMOUS_ENABLED=true
```

### Disable Autonomous Mode

```bash
# Method 1: Use the toggle script
uv run scripts/toggle_autonomous.py --disable

# Method 2: Edit config directly
jq '.enabled = false' config.json > tmp.json && mv tmp.json config.json

# Method 3: Set environment variable (session only)
set JUPYTER_AUTONOMOUS_ENABLED=false
```

### Check Current Status

```bash
# Check config
jq '.enabled' config.json

# Check environment
echo %JUPYTER_AUTONOMOUS_ENABLED%

# Run status check
uv run scripts/toggle_autonomous.py --status
```

---

## How Autonomous Mode Works

### Trigger Conditions

When autonomous mode is **ENABLED**, the AI will automatically:

1. **Detect Notebook Errors**
   - When a `.ipynb` file is modified
   - When Python code in notebooks fails
   - When imports from notebook modules fail

2. **Execute.Debug Loop**
   ```
   File changed → Execute notebook → Errors found → Parse → Fix → Re-execute → Validate
   ```

3. **Auto-Fix Patterns**
   | Error Type | Auto-Fix Action |
   |------------|-----------------|
   | `ModuleNotFoundError` | `uv add <package>` |
   | `NameError` | Search for definition, add import/definition |
   | `SyntaxError` | Fix syntax at indicated line |
   | `ImportError` | Check and fix import path |
   | `FileNotFoundError` | Create missing file/directory |

### Safety Boundaries

When autonomous mode is **DISABLED**, the AI will:

- ❌ NOT execute notebooks automatically
- ❌ NOT install packages without confirmation
- ❌ NOT modify notebook cells without explicit request
- ✅ Still provide error analysis and fix suggestions
- ✅ Still offer to run execution manually

---

## Configuration Options

Edit `config.json` to customize behavior:

```json
{
  "enabled": false,                    // Master switch
  "auto_execute_on_error": true,      // Auto-run when error detected
  "max_retry_iterations": 5,          // Max fix-and-retry loops
  "timeout_per_execution": 600,       // Seconds per execution
  "allowed_notebook_patterns": [...], // Glob patterns for allowed notebooks
  "excluded_notebook_patterns": [...],// Glob patterns for excluded notebooks
  "auto_fix_patterns": {              // Auto-fix rules by error type
    "ModuleNotFoundError": "install_package",
    "NameError": "check_definition",
    "SyntaxError": "fix_syntax",
    "FileNotFoundError": "check_path"
  },
  "reporting": {
    "log_all_executions": true,
    "save_error_reports": true,
    "output_directory": ".jupyter-execution-logs"
  },
  "safety": {
    "require_confirmation_for_package_install": true,
    "max_concurrent_executions": 1,
    "block_network_access": true
  }
}
```

---

## Use Cases

### Enable Autonomous Mode When:

- ✅ Actively developing notebook-based features
- ✅ Making frequent changes to notebook code
- ✅ Running CI/CD validation on notebooks
- ✅ Debugging complex notebook dependencies
- ✅ Batch processing multiple notebooks

### Disable Autonomous Mode When:

- ⏸️ Notebooks are stable and not changing
- ⏸️ Working on non-notebook code
- ⏸️ Concerned about execution costs/time
- ⏸️ Notebooks require user interaction
- ⏸️ Debugging visual/interactive elements

---

## Status Check Script

```bash
uv run scripts/toggle_autonomous.py --status
```

**Output:**
```
╔════════════════════════════════════════════════╗
║  Jupyter Autonomous Execution - Status        ║
╠════════════════════════════════════════════════╣
║  Mode:           ENABLED                       ║
║  Auto-fix:       ON                            ║
║  Max retries:    5                             ║
║  Timeout:        600s                          ║
║  Log dir:        .jupyter-execution-logs       ║
╚════════════════════════════════════════════════╝
```

---

## Integration with Kilo

The AI checks for autonomous mode before executing notebooks:

1. **Check config.json** - `enabled` field
2. **Check environment** - `JUPYTER_AUTONOMOUS_ENABLED`
3. **Check file marker** - `.jupyter-autonomous-enabled` in project root

If any indicates enabled, autonomous mode is active.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-21 | Initial activation system |
