# Notebook Debugging Templates

Templates and workflows for common debugging scenarios.

---

## debug_workflow.json

Structured workflow template for automated notebook debugging.

**Usage:** Reference this template when implementing debugging loops.

**Workflow Steps:**
1. Execute notebook → capture errors
2. Parse error JSON → extract cell_index, error_type
3. Locate source → read cell content
4. Analyze root cause → apply fix
5. Re-execute → validate
6. Repeat until success or max retries

---

## Adding Custom Templates

Create new JSON templates for specific workflows:

```json
{
    "name": "my-custom-workflow",
    "description": "What this workflow does",
    "steps": [
        {
            "name": "step_name",
            "action": "command or operation",
            "on_success": "next_step or complete",
            "on_failure": "retry or abort"
        }
    ],
    "max_iterations": 5
}
```

---

## Example: Import Error Resolution

```json
{
    "name": "import-error-resolution",
    "trigger": "ImportError or ModuleNotFoundError",
    "steps": [
        {
            "action": "extract_module_name",
            "pattern": "No module named '(.+)'",
            "store": "missing_module"
        },
        {
            "action": "search_imports",
            "command": "rga \"import {missing_module}\" src/"
        },
        {
            "action": "check_installation",
            "command": "uv pip list | grep {missing_module}"
        },
        {
            "action": "install_if_missing",
            "command": "uv add {missing_module}"
        },
        {
            "action": "re_execute",
            "command": "papermill notebook.ipynb output.ipynb"
        }
    ]
}
```

---

## Example: Syntax Error Fix Loop

```json
{
    "name": "syntax-error-fix",
    "trigger": "SyntaxError",
    "steps": [
        {
            "action": "parse_location",
            "extract": ["file_path", "line_number", "error_detail"]
        },
        {
            "action": "read_context",
            "command": "bat {file_path} --line-range {line-5}:{line+5}"
        },
        {
            "action": "identify_issue",
            "patterns": [
                "missing colon",
                "unclosed bracket",
                "invalid indentation",
                "typo in keyword"
            ]
        },
        {
            "action": "apply_fix",
            "strategy": "based_on_pattern"
        },
        {
            "action": "validate",
            "command": "python -m py_compile {file_path}"
        }
    ]
}
```

---

## Example: Cell Execution Order Fix

```json
{
    "name": "execution-order-fix",
    "trigger": "NameError (variable not defined)",
    "diagnosis": [
        "Check if variable defined in previous cells",
        "Check cell execution order",
        "Check for conditional definition"
    ],
    "fixes": [
        {
            "type": "reorder_cells",
            "description": "Move definition cell before usage"
        },
        {
            "type": "merge_cells",
            "description": "Combine definition and usage in same cell"
        },
        {
            "type": "add_default",
            "description": "Add default value before use"
        }
    ]
}
```

---

## Integration with Main Skill

These templates are referenced by the main SKILL.md debugging workflows. 
To use a template:

1. Read template JSON
2. Parse steps and conditions
3. Execute steps sequentially
4. Track success/failure at each step
5. Apply fixes based on template guidance
6. Re-execute and validate
